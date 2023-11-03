import uuid
import logging
import os
import re
import shutil
from wesync.services.interaction.terminal import bcolors
from wesync.services.config.configManager import ConfigManager
from datetime import datetime
from typing import Union

timestampString = "%Y-%m-%d_%H-%M"


class Snapshot:
    def __init__(self, path: str = None, projectName: str = None, deploymentName: str = None, label: str = None, timestamp: datetime = None):
        self.projectName = projectName
        self.deploymentName = deploymentName
        self.timestamp = timestamp
        self.label = label
        self.path = path

    @staticmethod
    def nameFromParts(deploymentName: str, label: str, timestamp: datetime):
        return deploymentName + "__" + timestamp.strftime(timestampString) + "__" + label

    def getPartsFromPath(self):
        try:
            lastDirName = self.getFolderName()
            parentFolderName = self.path.split("/")[-2]
        except:
            logging.error("Failed to extract project information from {}".format(self.path))
            return None

        self.projectName = parentFolderName
        (self.deploymentName, self.timestamp, self.label) = SnapshotManager.getPartsFromFolder(lastDirName)
        return None

    def getFolderName(self):
        return os.path.basename(self.path)

    def getPath(self, filename: str = None):
        if filename is None:
            return self.path
        else:
            return self.path + "/" + filename

    def getTimestamp(self):
        if not self.timestamp:
            self.getPartsFromPath()

        if not self.timestamp:
            raise ValueError("Failed to get timestamp for snapshot at {}".format(self.path))

        return self.timestamp

    def hasFile(self, filename: str) -> bool:
        return os.path.exists(self.getPath(filename))

    def exists(self) -> bool:
        return os.path.exists(self.getPath())

    def delete(self):
        logging.warning("Deleting snapshot at {}".format(self.getPath()))
        return shutil.rmtree(self.getPath())

    def files(self):
        return os.listdir(self.path)

    def createDirectory(self):
        try:
            logging.debug("Creating directory at {}".format(self.getPath()))
            os.makedirs(self.getPath(), exist_ok=True)
        except:
            logging.warning("Failed to create directory %s", self.getPath())

    def getDeploymentName(self):
        return self.deploymentName

    def __str__(self):
        return "{}{} {}{} {}{} {}{}".format(
            bcolors.WARNING,
            self.projectName,
            bcolors.OKGREEN,
            self.deploymentName,
            bcolors.FAIL,
            self.label,
            bcolors.OKCYAN,
            self.timestamp
        )


class SnapshotManager:
    def __init__(self, config: ConfigManager):
        self.config = config

    def initSnapshot(self, projectName, deploymentName, label: str = None, timestamp: datetime = None) -> Snapshot:
        if label is None:
            label = uuid.uuid4().hex[:12]

        timestamp = timestamp if timestamp else datetime.now()
        path = self.config.getStashDir() + "/" + projectName + "/" + Snapshot.nameFromParts(deploymentName, label, timestamp=timestamp)

        snapshot = Snapshot(
            projectName=projectName,
            deploymentName=deploymentName,
            label=label,
            timestamp=timestamp,
            path=path
        )
        if not self.config.get('dry-run'):
            snapshot.createDirectory()
        return snapshot

    def getProjectSnapshotPath(self, projectName: str) -> str:
        return self.config.getStashDir() + "/" + projectName

    def getSnapshotByLabel(self, projectName: str, label: str) -> Union[Snapshot, None]:
        projectDirectory = self.getProjectSnapshotPath(projectName)
        if not os.path.exists(projectDirectory):
            return None
        for file in os.listdir(projectDirectory):
            if re.match(r'.*__{}$'.format(label), file) is not None:
                return self.getSnapshotByPath(projectDirectory + "/" + file)
        return None

    def getSnapshotByPath(self, path: str) -> Snapshot:
        snapshot = Snapshot(path)
        snapshot.getPartsFromPath()
        return snapshot

    def getSnapshotByFolder(self, projectName: str, folderName: str) -> Snapshot | None:
        for snapshot in self.getSnapshotsByProject(projectName):
            if snapshot.getFolderName() == folderName:
                return snapshot

    def getSnapshotsByProject(self, projectName: str) -> list:
        snapshots = []
        projectDirectory = self.getProjectSnapshotPath(projectName)
        if not os.path.exists(projectDirectory):
            return snapshots

        for file in os.listdir(projectDirectory):
            snapshots.append(self.getSnapshotByPath(projectDirectory + "/" + file))
        return snapshots

    def getSnapshotsByDeployment(self, projectName: str, deploymentName: str) -> list:
        snapshots = []

        projectDirectory = self.getProjectSnapshotPath(projectName)
        if not os.path.exists(projectDirectory):
            return snapshots

        for file in os.listdir(projectDirectory):
            if re.match(r'^{}__.*$'.format(deploymentName), file) is not None:
                snapshots.append(self.getSnapshotByPath(projectDirectory + "/" + file))
        return snapshots

    def deleteByPath(self, path: str):
        snapshot = self.getSnapshotByPath(path)
        if snapshot and snapshot.exists():
            snapshot.delete()

    def getAllSnapshots(self):
        rootDirectory = self.config.getStashDir()
        snapshots = []
        for project in os.listdir(rootDirectory):
            projectDirectory = rootDirectory + "/" + project
            for file in os.listdir(projectDirectory):
                snapshots.append(self.getSnapshotByPath(projectDirectory + "/" + file))

        return snapshots

    def deleteByLabel(self, projectName: str, label: str):
        snpashot = self.getSnapshotByLabel(projectName, label)
        if snpashot and snpashot.exists():
            snpashot.delete()

    def deleteByProject(self, projectName: str):
        for snapshot in self.getSnapshotsByProject(projectName):
            if snapshot.exists():
                snapshot.delete()

    def getLatestSnapshot(self, projectName: str) -> Snapshot:
        snapshots = sorted(self.getSnapshotsByProject(projectName),
                           key=lambda s: s.getTimestamp(),
                           reverse=True)
        if len(snapshots) > 0:
            return snapshots[0]

    @staticmethod
    def getPartsFromFolder(path: str) -> tuple:
        matchResult = re.match(r"^(.*?)__(.*?)__(.*)$", path)
        deploymentName = None
        timestamp = None
        label = None

        if matchResult:
            deploymentName = matchResult.group(1)
            timestamp = matchResult.group(2)
            try:
                timestamp = datetime.strptime(timestamp, timestampString)
            except ValueError:
                pass
            timestamp = timestamp
            if len(matchResult.groups()) > 2:
                label = matchResult.group(3)
        return deploymentName, timestamp, label

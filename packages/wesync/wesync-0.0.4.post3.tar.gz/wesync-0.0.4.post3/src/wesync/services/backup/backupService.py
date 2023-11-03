import logging
from datetime import datetime
from os.path import normpath
from wesync.services.snapshot import Snapshot, SnapshotManager
from wesync.services.config.sections.projectConfig import ProjectConfigData
from wesync.services.config.configManager import ConfigManager
from wesync.services.execute.backupCommandExecutor import BackupCommandExecutor
from wesync.services.config.sections.backupConfig import BackupConfigData
from wesync.services.operations.commonOperations import CommonOperationsService
from wesync.services.execute.RsyncFileTransferService import RsyncFileTransfer


class BackupService(object):

    def __init__(self, config: ConfigManager, project: ProjectConfigData, backup: BackupConfigData):
        self.project = project
        self.backup = backup
        self.config = config
        self.snapshotManager = SnapshotManager(self.config)
        self.backupOperations = CommonOperationsService(self.config, executor=BackupCommandExecutor(self.config, self.backup))

    def _getBackupPath(self, backupSnapshotName: str = "") -> str:
        backupPath = self.backup.getPath()
        projectPath = self.project.getBackupConfigByName(
            self.backup.getName()
        ).get('path', '')
        return normpath('/'.join([backupPath, projectPath, backupSnapshotName]))

    def storeSnapshot(self, snapshot: Snapshot, backupSnapshotName: str, force: bool = False):

        if self.project.getName() != snapshot.projectName:
            raise Exception(f"Project name does not match between {self.project.getName()} and {snapshot.projectName}")

        if not snapshot.exists():
            raise Exception(f"Snapshot is missing locally {snapshot}")

        backupPath = self._getBackupPath(backupSnapshotName)
        logging.info(f"Backing up snapshot at {backupPath}")

        if self.backupOperations.pathExists(backupPath):
            if force is False:
                logging.info("Backup already uploaded. Use --replace to force replacement")
                return True
            logging.warning("Directory already exists. Will replace it.")
            self.backupOperations.deletePath(backupPath, recursive=True)

        self.backupOperations.createPath(backupPath)

        rsyncFileTransfer = RsyncFileTransfer(self.config)
        rsyncFileTransfer.copyToRemote(
            sourcePath=snapshot.getPath() + "/",
            destination=self.backup,
            destinationPath=backupPath
        )

    def updateLatest(self, backupSnapshotName: str):
        fromBackupPath = self._getBackupPath(backupSnapshotName)
        toBackupPath = self._getBackupPath('latest')
        logging.info(f"Copying backup at {backupSnapshotName} to latest")
        if self.backupOperations.pathExists(toBackupPath):
            self.backupOperations.deletePath(toBackupPath, recursive=True)

        self.backupOperations.copyPath(
            fromPath=fromBackupPath,
            toPath=toBackupPath,
            recursive=True
        )

    def downloadSnapshot(self, backupSnapshotName: str, force: bool = False) -> Snapshot:
        backupPath = self._getBackupPath(backupSnapshotName)
        logging.info(f"Getting backup from {backupPath}")

        existingSnapshot = self.snapshotManager.getSnapshotByFolder(self.project.getName(), backupSnapshotName)
        if existingSnapshot:
            if force is False:
                logging.info("Snapshot with label already exists locally. Use --replace to force replacement.")
                return existingSnapshot
            existingSnapshot.delete()

        (deploymentName, timestamp, label) = SnapshotManager.getPartsFromFolder(backupSnapshotName)

        if deploymentName is None:
            deploymentName = self.backup.getName()
        if timestamp is None:
            timestamp = datetime.now()

        snapshot = self.snapshotManager.initSnapshot(
            self.project.getName(),
            deploymentName,
            label,
            timestamp,
        )

        rsyncFileTransfer = RsyncFileTransfer(self.config)
        rsyncFileTransfer.copyFromRemote(
            source=self.backup,
            sourcePath=backupPath + "/",
            destinationPath=snapshot.getPath()
        )

        return snapshot

    def listBackups(self) -> list:
        return self.backupOperations.listDir(self._getBackupPath())

    def searchForBackupInFiles(self, chosenBackup: str) -> str | None:
        if chosenBackup is None:
            return None

        backups = self.listBackups()

        for backup in backups:
            (deployment, timestamp, label) = SnapshotManager.getPartsFromFolder(backup)
            if label == chosenBackup:
                return backup

        for backup in backups:
            if backup == chosenBackup:
                return backup

        return None


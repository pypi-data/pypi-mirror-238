import logging
import uuid
import os.path
import re
from wesync.services.snapshot import Snapshot
from .commonOperations import CommonOperationsService
from wesync.services.execute.localCommandExecutor import LocalCommandExecutor
from wesync.services.execute.remoteProjectCommandExecutor import RemoteProjectCommandExecutor
from wesync.services.config.sections.deploymentConfig import DeploymentConfigData
from wesync.services.config.configManager import ConfigManager


class ProjectOperationsService(CommonOperationsService):

    projectType = None

    defaultFilePathArtifacts = [{
        "name": "project.tar.gz",
        "path": "."
    }]

    def __init__(self, deployment: DeploymentConfigData, config: ConfigManager, **kwargs):
        self.deployment = deployment
        self.config = config
        super().__init__(config=config, executor=self.getExecutor())
        self.artifactsConfig = self.deployment.getProject().getArtifacts()
        self.project = self.deployment.getProject()

    def getExecutor(self):
        if self.deployment.isLocal() is True:
            return LocalCommandExecutor(self.config)
        else:
            return RemoteProjectCommandExecutor(self.config, self.deployment)

    def getFilePathArtifacts(self) -> list:
        filePathArtifacts = []
        for artifactConfig in self.artifactsConfig:
            if artifactConfig.get('type') == 'filepath':
                filePathArtifacts.append(artifactConfig)

        if not filePathArtifacts:
            return self.defaultFilePathArtifacts
        return filePathArtifacts

    def exportFileArtifacts(self, snapshot: Snapshot):
        for artifactConfig in self.getFilePathArtifacts():
            path = artifactConfig.get('path')
            name = artifactConfig.get('name')
            if not name or not path:
                raise ValueError("Path or name missing from artifact config")
            snapshotPath = snapshot.getPath(name)
            self.exportFiles(snapshotPath, path)

    def importFileArtifacts(self, snapshot: Snapshot):
        for artifactConfig in self.getFilePathArtifacts():
            path = artifactConfig.get('path')
            name = artifactConfig.get('name')
            if not name or not path:
                raise ValueError("Path or name missing from artifact config")
            snapshotPath = snapshot.getPath(name)
            self.importFiles(snapshotPath, path)

    def createTempSnapshot(self) -> Snapshot:
        pathName = '/var/tmp/westash'
        projectName = self.deployment.getProject().getName()
        if not self.pathExists(pathName):
            self.createPath(pathName)
            self.runCommand(['chmod', '777', pathName])

        tmpDirName = pathName + '/' + projectName + "_" + uuid.uuid4().hex[:8]
        self.deletePath(tmpDirName, recursive=True, force=True)
        self.createPath(tmpDirName)
        remoteSnapshot = Snapshot(path=tmpDirName)
        return remoteSnapshot

    def exportFiles(self, archiveExportFile, path):
        path = os.path.normpath(re.sub(r'^(/+)', '', path))

        rootDir = self.deployment.getPath()
        pathDirectories = path.split("/")

        if len(pathDirectories) > 1:
            path = pathDirectories[-1]
            rootDir = rootDir + "/" + '/'.join(pathDirectories[:-1])

        self.archiveFiles(rootPath=rootDir, files=[path], outputArchiveFile=archiveExportFile)

    def importFiles(self, archiveImportFile, path):
        rootDir = self.deployment.getPath()

        path = os.path.normpath(re.sub(r'^(/+)', '', path))
        pathDirectories = path.split("/")

        if len(pathDirectories) > 1:
            path = pathDirectories[-1]
            rootDir = rootDir + "/" + '/'.join(pathDirectories[:-1])

        self.unarchiveFiles(inputArchiveFile=archiveImportFile, rootPath=rootDir, files=[path], delete=True)

    def cloneRepository(self, repositoryURL: str, branch: str = 'master'):
        args = ['git', 'clone', repositoryURL, '--branch', branch]
        logging.info("Cloning repository into" % repositoryURL)
        self.runCommand(args)

    def fullExport(self, snapshot: Snapshot):
        self.exportFileArtifacts(snapshot)

    def fullImport(self, snapshot: Snapshot):
        self.importFileArtifacts(snapshot)

    def getDeployment(self) -> DeploymentConfigData:
        return self.deployment

    def runCommand(self, args, **kwargs):
        return super(ProjectOperationsService, self).runCommand(args, cwd=self.deployment.getPath(), **kwargs)
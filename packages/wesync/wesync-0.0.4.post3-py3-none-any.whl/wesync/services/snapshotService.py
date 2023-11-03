import logging
from wesync.services.config.configManager import ConfigManager
from wesync.services.snapshot import Snapshot
from wesync.services.execute.RsyncFileTransferService import RsyncFileTransfer
from wesync.services.operations.projectOperations import ProjectOperationsService


class SnapshotService(object):
    def __init__(self, config: ConfigManager):
        self.config = config

    def exportRemoteSnapshot(self, projectManager: ProjectOperationsService, snapshot: Snapshot):
        filetransfer = RsyncFileTransfer(self.config)
        remoteSnapshot = projectManager.createTempSnapshot()

        projectManager.fullExport(remoteSnapshot)
        logging.info("Copying snapshot from remote deployment")
        filetransfer.copyFromRemote(
            projectManager.getDeployment(),
            sourcePath=remoteSnapshot.getPath() + "/",
            destinationPath=snapshot.getPath()
        )

        projectManager.deletePath(remoteSnapshot.getPath(), recursive=True)

    def importRemoteSnapshot(self, projectManager: ProjectOperationsService, snapshot: Snapshot):
        filetransfer = RsyncFileTransfer(self.config)
        projectName = projectManager.deployment.getProject().getName()
        tmpDirName = '/var/tmp/westash/' + projectName
        projectManager.createPath(tmpDirName)

        remoteSnapshot = Snapshot(tmpDirName)
        logging.info("Copying snapshot to remote deployment")
        filetransfer.copyToRemote(
            snapshot.getPath() + "/",
            projectManager.getDeployment(),
            destinationPath=tmpDirName
        )

        projectManager.fullImport(remoteSnapshot)
        projectManager.deletePath(tmpDirName, recursive=True)

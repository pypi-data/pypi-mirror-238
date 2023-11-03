import logging
from argparse import ArgumentParser
from wesync.services.projectManagerFactory import ProjectManagerFactory
from wesync.services.config.configManager import ConfigManager
from wesync.commands.operationManager import Operation
from wesync.services.snapshot import SnapshotManager
from wesync.services.backup.backupService import BackupService
from wesync.services.snapshotService import SnapshotService


class BackupExportOperation(Operation):
    operationName = 'export'

    def __init__(self, config: ConfigManager, **kwargs):
        super().__init__()
        self.config = config

        self.deployment = self.config.getDeployment()
        self.deployment.ensureKeysAreSet(["name", "path"])

        self.project = self.deployment.getProject()
        self.project.ensureKeysAreSet(['name'])

        self.projectManager = ProjectManagerFactory.getProjectManagerFor(self.deployment, self.config)
        self.snapshotManager = SnapshotManager(self.config)
        self.snapshotService = SnapshotService(self.config)

    def run(self):
        snapshot = self.snapshotManager.initSnapshot(
            self.project.getName(),
            self.deployment.getName(),
            self.config.get('label')
        )

        if not (backupName := self.config.get('backup')):
            backupName = self.project.getDefaultBackupName('write')

        backupConfigData = self.config.localConfigData.getBackupByName(backupName)
        if not backupConfigData:
            logging.error(f"Failed to get backup {backupName} for project {self.project.getName()}")
            return False

        if backupConfigData.isReadonly() is True:
            logging.error(f"Backup {backupName} is read only")
            return False

        backupPath = snapshot.getFolderName()

        if self.deployment.isLocal():
            self.projectManager.fullExport(snapshot)
        else:
            self.snapshotService.exportRemoteSnapshot(self.projectManager, snapshot)

        logging.log(5, f"Using snapshot {snapshot}")

        backupService = BackupService(self.config, self.project, backupConfigData)
        backupService.storeSnapshot(snapshot, backupPath, self.config.get('replace', False))
        if self.config.get('latest') is True:
            backupService.updateLatest(backupPath)

        if self.config.get('delete') is True:
            snapshot.delete()

    @staticmethod
    def configureArguments(argumentParser: ArgumentParser):
        argumentParser.add_argument("--deployment", help="Deployment to lookup in config")
        argumentParser.add_argument("--delete", help="Delete snapshot after import", action='store_true')
        argumentParser.add_argument("--label", help="Label of the export snapshot")
        argumentParser.add_argument("--backup", help="Name of the backup server")
        argumentParser.add_argument("--replace", help="Replace the backup", action='store_true')
        argumentParser.add_argument("--latest", help="Mark the backup as latest", action='store_true')
        return argumentParser


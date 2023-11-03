import logging
from argparse import ArgumentParser
from wesync.services.config.configManager import ConfigManager
from wesync.commands.operationManager import Operation
from wesync.services.snapshot import SnapshotManager
from wesync.services.backup.backupService import BackupService


class BackupPushOperation(Operation):
    operationName = 'push'

    def __init__(self, config: ConfigManager, **kwargs):
        super().__init__()
        self.config = config

        self.project = self.config.getCurrentProject()
        self.project.ensureKeysAreSet(['name'])

        self.snapshotManager = SnapshotManager(self.config)

    def run(self):
        if label := self.config.get('label'):
            snapshot = self.snapshotManager.getSnapshotByLabel(self.project.getName(), label)
        else:
            snapshot = self.snapshotManager.getLatestSnapshot(self.project.getName())
        logging.log(5, f"Using snapshot {snapshot}")

        if not (backupName := self.config.get('backup')):
            backupName = self.project.getDefaultBackupName('write')

        backupConfigData = self.config.localConfigData.getBackupByName(backupName)
        if not backupConfigData:
            logging.error(f"Failed to get backup {backupName} for project {self.project.getName()}")
            return False

        if backupConfigData.isReadonly() is True:
            logging.error(f"Backup {backupName} is read only")
            return False

        if not (backupPath := self.config.get('path')):
            backupPath = snapshot.getFolderName()

        backupService = BackupService(self.config, self.project, backupConfigData)
        backupService.storeSnapshot(snapshot, backupPath, self.config.get('replace', False))
        if self.config.get('latest') is True:
            backupService.updateLatest(backupPath)

    @staticmethod
    def configureArguments(argumentParser: ArgumentParser):
        argumentParser.add_argument("--label", help="Label of the snapshot")
        argumentParser.add_argument("--path", help="Backup path")
        argumentParser.add_argument("--backup", help="Name of the backup server")
        argumentParser.add_argument("--replace", help="Replace the backup", action='store_true')
        argumentParser.add_argument("--latest", help="Mark the backup as latest", action='store_true')
        return argumentParser


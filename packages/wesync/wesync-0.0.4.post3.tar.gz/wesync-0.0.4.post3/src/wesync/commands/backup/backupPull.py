import logging
from argparse import ArgumentParser
from wesync.services.config.configManager import ConfigManager
from wesync.commands.operationManager import Operation
from wesync.services.snapshot import SnapshotManager
from wesync.services.backup.backupService import BackupService


class BackupPullOperation(Operation):
    operationName = 'pull'

    def __init__(self, config: ConfigManager, **kwargs):
        super().__init__()
        self.config = config

        self.project = self.config.getCurrentProject()
        self.project.ensureKeysAreSet(['name'])

        self.snapshotManager = SnapshotManager(self.config)

    def run(self):
        if not (backupName := self.config.get('backup')):
            backupName = self.project.getDefaultBackupName('read')

        backupConfigData = self.config.localConfigData.getBackupByName(backupName)
        if not backupConfigData:
            logging.error(f"Failed to get backup {backupName} for project {self.project.getName()}")
            return False

        chosenBackup = self.config.get('path')

        backupService = BackupService(self.config, self.project, backupConfigData)
        backupPath = backupService.searchForBackupInFiles(chosenBackup)

        if not backupPath:
            logging.error(f"Failed to find backup path {chosenBackup}")
            return False

        backupService.downloadSnapshot(backupPath, self.config.get('replace', False))

    @staticmethod
    def configureArguments(argumentParser: ArgumentParser):
        argumentParser.add_argument("--path", help="Backup path", default='latest')
        argumentParser.add_argument("--backup", help="Name of the backup server")
        argumentParser.add_argument("--replace", help="Replace the backup", action='store_true')
        return argumentParser

import logging
from argparse import ArgumentParser
from wesync.services.config.configManager import ConfigManager
from wesync.commands.operationManager import Operation
from wesync.services.snapshot import SnapshotManager, Snapshot
from wesync.services.backup.backupService import BackupService
from wesync.services.interaction.userInteraction import UserInteraction


class BackupListOperation(Operation):
    operationName = 'list'

    def __init__(self, config: ConfigManager, **kwargs):
        super().__init__()
        self.config = config

        self.project = self.config.getCurrentProject()
        self.project.ensureKeysAreSet(['name'])

    def run(self):
        if not (backupName := self.config.get('backup')):
            backupName = self.project.getDefaultBackupName('read')

        backupConfigData = self.config.localConfigData.getBackupByName(backupName)
        if not backupConfigData:
            logging.error(f"Failed to get backup {backupName} for project {self.project.getName()}")
            return False

        backupService = BackupService(self.config, self.project, backupConfigData)
        for file in backupService.listBackups():
            (deployment, timestamp, label) = SnapshotManager.getPartsFromFolder(file)
            if deployment is None and timestamp is None:
                UserInteraction.print("{}".format(file))
            else:
                s = Snapshot(
                    projectName=backupService.project.getName(),
                    deploymentName=deployment,
                    timestamp=timestamp, label=label
                )
                logging.info(str(s))

    @staticmethod
    def configureArguments(argumentParser: ArgumentParser):
        argumentParser.add_argument("--backup", help="Name of the backup server")
        return argumentParser


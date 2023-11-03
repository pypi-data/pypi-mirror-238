import logging
from argparse import ArgumentParser
from wesync.services.projectManagerFactory import ProjectManagerFactory
from wesync.services.config.configManager import ConfigManager
from wesync.commands.operationManager import Operation
from wesync.services.snapshot import SnapshotManager
from wesync.services.backup.backupService import BackupService
from wesync.services.snapshotService import SnapshotService
from wesync.services.interaction.userInteraction import UserInteraction
from wesync.services.processors.processorManager import ProcessorManager


class BackupImportOperation(Operation):
    operationName = 'import'

    def __init__(self, config: ConfigManager, **kwargs):
        super().__init__()
        self.config = config
        self.userInteraction = UserInteraction()
        self.processorManager = ProcessorManager(self.config)

        self.deployment = self.config.getDeployment()
        self.deployment.ensureKeysAreSet(["name", "path"])

        self.project = self.deployment.getProject()
        self.project.ensureKeysAreSet(['name'])

        self.projectManager = ProjectManagerFactory.getProjectManagerFor(self.deployment, self.config)
        self.snapshotManager = SnapshotManager(self.config)
        self.snapshotService = SnapshotService(self.config)

    def run(self):
        if not (backupName := self.config.get('backup')):
            backupName = self.project.getDefaultBackupName('read')

        backupConfigData = self.config.localConfigData.getBackupByName(backupName)
        if not backupConfigData:
            logging.error(f"Failed to get backup {backupName} for project {self.project.getName()}")
            return False

        if self.deployment.isProtected():
            if self.userInteraction.confirm("Target deployment is protected. Continue ?", level='warn') is False:
                return False

        if self.config.get('latest', False) is True:
            chosenBackup = 'latest'
        else:
            chosenBackup = self.config.get('label')

        if chosenBackup is None:
            logging.error(f"Backup must be specified with --label or --latest")
            return False

        backupService = BackupService(self.config, self.project, backupConfigData)
        backupPath = backupService.searchForBackupInFiles(chosenBackup)

        if not backupPath:
            logging.error(f"Failed to find backup path {chosenBackup}")
            return False

        snapshot = backupService.downloadSnapshot(backupPath, self.config.get('replace', False))

        if self.deployment.isLocal():
            self.projectManager.fullImport(snapshot)
        else:
            self.snapshotService.importRemoteSnapshot(self.projectManager, snapshot)

        if self.config.get('delete') is True:
            snapshot.delete()

        sourceHostName = None
        if deploymentName := snapshot.getDeploymentName():
            if deployment := self.config.localConfigData.getDeploymentByName(self.project.getName(), deploymentName):
                sourceHostName = deployment.get('hostname')

        importProcessors = self.processorManager.getForAnyTrigger(['import'], self.deployment)
        importProcessors.executeAll(searchAndReplaceOld=sourceHostName)

    @staticmethod
    def configureArguments(argumentParser: ArgumentParser):
        argumentParser.add_argument("--deployment", help="Deployment to lookup in config")
        argumentParser.add_argument("--delete", help="Delete snapshot after import", action='store_true')
        argumentParser.add_argument("--label", help="Label of the export snapshot")
        argumentParser.add_argument("--backup", help="Name of the backup server")
        argumentParser.add_argument("--replace", help="Replace the backup", action='store_true')
        argumentParser.add_argument("--latest", help="Get the latest backup", action='store_true')
        return argumentParser


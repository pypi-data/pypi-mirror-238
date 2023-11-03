import logging
from argparse import ArgumentParser
from wesync.services.interaction.userInteraction import UserInteraction
from wesync.services.projectManagerFactory import ProjectManagerFactory
from wesync.services.snapshot import SnapshotManager, Snapshot
from wesync.services.config.configManager import ConfigManager
from wesync.commands.operationManager import Operation
from wesync.services.processors.processorManager import ProcessorManager
from wesync.services.snapshotService import SnapshotService


class SnapshotImportOperation(Operation):

    operationName = 'import'

    def __init__(self, config: ConfigManager, **kwargs):
        super().__init__()
        self.config = config
        self.processorManager = ProcessorManager(self.config)

        self.userInteraction = UserInteraction()

        self.deployment = self.config.getDeployment()
        self.deployment.ensureKeysAreSet(["name", "path"])

        self.project = self.deployment.getProject()
        self.project.ensureKeysAreSet(['name', 'type'])

        self.projectManager = ProjectManagerFactory.getProjectManagerFor(self.deployment, self.config)
        self.snapshotManager = SnapshotManager(self.config)
        self.snapshotService = SnapshotService(self.config)

    def run(self):
        projectName = self.project.getName()

        if snapshotLabel := self.config.get('label'):
            snapshot = self.snapshotManager.getSnapshotByLabel(projectName, snapshotLabel)
        elif snapshotPath := self.config.get('path'):
            snapshot = self.snapshotManager.getSnapshotByPath(snapshotPath)
        else:
            snapshot = self.snapshotManager.getLatestSnapshot(projectName)

        if not snapshot:
            logging.error("Snapshot label or path must be specified")

        if self.deployment.isProtected():
            if self.userInteraction.confirm("Target deployment is protected. Continue ?", level='warn') is False:
                return False

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
        argumentParser.add_argument("--delete", help="Delete snapshot after import", action='store_true')
        argumentParser.add_argument("--path", help="Import according to path")
        argumentParser.add_argument("--label", help="Label of the import")
        return argumentParser


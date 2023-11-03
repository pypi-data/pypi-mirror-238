import logging
from argparse import ArgumentParser
from wesync.services.projectManagerFactory import ProjectManagerFactory
from wesync.services.snapshot import SnapshotManager
from wesync.services.config.configManager import ConfigManager
from wesync.commands.operationManager import Operation
from wesync.services.snapshotService import SnapshotService


class SnapshotExportOperation(Operation):

    operationName = 'export'

    def __init__(self, config: ConfigManager, **kwargs):
        super().__init__()
        self.config = config

        self.deployment = self.config.getDeployment()
        self.deployment.ensureKeysAreSet(["name", "path"])

        self.project = self.deployment.getProject()
        self.project.ensureKeysAreSet(['name', 'type'])

        self.projectManager = ProjectManagerFactory.getProjectManagerFor(self.deployment, self.config)
        self.snapshotManager = SnapshotManager(self.config)
        self.snapshotService = SnapshotService(self.config)

    def run(self):

        newSnapshot = self.snapshotManager.initSnapshot(
            self.project.getName(),
            self.deployment.getName(),
            self.config.get('label')
        )
        if self.deployment.isLocal():
            self.projectManager.fullExport(newSnapshot)
        else:
            self.snapshotService.exportRemoteSnapshot(self.projectManager, newSnapshot)

        return newSnapshot

    @staticmethod
    def configureArguments(argumentParser: ArgumentParser):
        argumentParser.add_argument("--label", help="Label of the export")
        return argumentParser
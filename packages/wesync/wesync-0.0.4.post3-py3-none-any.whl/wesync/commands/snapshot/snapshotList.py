import logging
from wesync.services.snapshot import SnapshotManager
from wesync.services.config.configManager import ConfigManager
from wesync.commands.operationManager import Operation


class SnapshotListOperation(Operation):

    operationName = 'list'

    def __init__(self, config: ConfigManager, **kwargs):
        super().__init__()
        self.config = config

        self.project = self.config.getCurrentProject(required=False)

        self.snapshotManager = SnapshotManager(self.config)

    def run(self):
        if self.project:
            projectName = self.project.getName()
            snapshots = self.snapshotManager.getSnapshotsByProject(projectName)
            logging.info("{} snapshots for project {}".format(len(snapshots), projectName))
        else:
            snapshots = self.snapshotManager.getAllSnapshots()
            logging.info("{} snapshots for all projects".format(len(snapshots)))

        for snapshot in sorted(snapshots, key=lambda s: s.getTimestamp()):
            logging.info(str(snapshot))

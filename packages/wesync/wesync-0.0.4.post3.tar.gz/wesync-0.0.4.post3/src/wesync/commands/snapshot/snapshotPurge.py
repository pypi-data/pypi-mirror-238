from wesync.services.snapshot import SnapshotManager
from wesync.services.config.configManager import ConfigManager
from wesync.commands.operationManager import Operation
from wesync.services.interaction.userInteraction import UserInteraction


class SnapshotPurgeOperation(Operation):

    operationName = 'purge'

    def __init__(self, config: ConfigManager, **kwargs):
        super().__init__()
        self.config = config

        self.project = self.config.getCurrentProject(required=False)

        self.snapshotManager = SnapshotManager(self.config)

    def run(self):
        if self.project:
            projectName = self.project.getName()
            if UserInteraction().confirm("Delete all snapshots for project {}".format(projectName)) is True:
                self.snapshotManager.deleteByProject(projectName)
        else:
            if UserInteraction().confirm("Delete all snapshots") is True:
                for snapshot in self.snapshotManager.getAllSnapshots():
                    snapshot.delete()

from wesync.services.interaction.userInteraction import UserInteraction
from wesync.services.config.resolvers.projectConfigResolver import ProjectConfigResolver
from wesync.services.config.sections.configData import SectionConfigData
from .hasProcessors import HasProcessors


class ProjectConfigData(HasProcessors, SectionConfigData):

    mandatoryKeys = ["name", "type"]
    optionalKeys = ["artifacts", "syncStrategy"]

    def __init__(self):
        super(ProjectConfigData, self).__init__()
        self.interaction = UserInteraction()
        self.deployments = []
        self.backups = []

    def getName(self) -> str:
        return self.get('name').lower()

    def getType(self):
        return self.get('type')

    def getDeployments(self):
        return self.deployments

    def getPath(self):
        return self.get('path')

    def getArtifacts(self):
        return self.get('artifacts', [])

    def getSyncStrategy(self):
        return self.get('syncStrategy', 'snapshot')

    def getBackupConfigByName(self, backupName: str):
        for backupConfig in self.backups:
            if backupConfig.get('name') == backupName:
                return backupConfig

    def getDefaultBackupName(self, action: str = 'write') -> str | None:
        for backupConfig in self.backups:
            if backupConfig.isDefault(action) is True:
                return backupConfig.get('name')

    def ensureKeysAreSet(self, keys: list = None):
        if keys is None:
            keys = self.mandatoryKeys

        for key in keys:
            if not self.has(key):
                defaultResolve = ProjectConfigResolver(**self.getData())
                self.setKeyFromInput(key, defaultResolve.resolveKey(key), "project")

    def attachDeployment(self, deployment):
        self.deployments.append(deployment)

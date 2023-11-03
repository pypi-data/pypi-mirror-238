from wesync.services.config.sections.configData import SectionConfigData
from wesync.services.config.sections.projectConfig import ProjectConfigData


class ProjectBackupConfigData(SectionConfigData):

    mandatoryKeys = ['name', 'path']
    optionalKeys = ['default', 'defaultRead', 'defaultWrite', 'readonly']

    def __init__(self, project: ProjectConfigData):
        self.project = project
        super().__init__()

    def getName(self):
        return self.get('name')

    def getPath(self):
        return self.get('path')

    def isReadonly(self) -> bool:
        return self.get('readonly') is True

    def isDefault(self, action: str) -> bool:
        if action == 'read':
            return self.get('defaultRead') is True or self.get('default') is True
        elif action == 'write':
            return self.get('defaultWrite') is True or self.get('default') is True

        return self.get('default') is True

    def ensureKeysAreSet(self, keys: list = None):
        if keys is None:
            keys = self.mandatoryKeys
        for key in keys:
            if not self.has(key):
                raise ValueError(f"Missing key {key} for ProjectBackupConfigData")

    def __str__(self):
        return "ProjectBackup {} {} \n".format(
            self.getName(),
            self.get('path')
        )

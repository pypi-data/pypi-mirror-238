from wesync.services.config.sections.configData import SectionConfigData


class BackupConfigData(SectionConfigData):

    mandatoryKeys = ['name', 'path', 'host', 'port', 'username']
    optionalKeys = ['readonly']

    def __init__(self):
        super().__init__()

    def getName(self):
        return self.get('name')

    def getPath(self):
        return self.get('path')

    def isReadonly(self) -> bool:
        return self.get('readonly') is True

    def ensureKeysAreSet(self, keys: list = None):
        if keys is None:
            keys = self.mandatoryKeys
        for key in keys:
            if not self.has(key):
                raise ValueError(f"Missing key {key} for BackupConfigData")

    def __str__(self):
        return "Backup {} {}@{}:{} {} \n".format(
            self.getName(),
            self.get('username'),
            self.get('host'),
            self.get('port'),
            self.get('path')
        )

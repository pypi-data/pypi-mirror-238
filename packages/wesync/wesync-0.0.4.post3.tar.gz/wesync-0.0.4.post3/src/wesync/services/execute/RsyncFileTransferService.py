from wesync.services.config.sections.deploymentConfig import DeploymentConfigData
from wesync.services.config.configManager import ConfigManager
from wesync.services.config.sections.backupConfig import BackupConfigData
from .localCommandExecutor import LocalCommandExecutor


class RsyncFileTransfer:

    def __init__(self, config: ConfigManager):
        self.config = config
        self.localCommandExecutor = LocalCommandExecutor(self.config)

    def copyFromRemote(self, source, sourcePath: str, destinationPath: str):
        if isinstance(source, (DeploymentConfigData, BackupConfigData)):
            args = [
                "rsync", "-a", "-q", "--delete",
                "-e", "ssh -p {} -o StrictHostKeyChecking=no".format(
                    str(source.get('port'))
                ),
                "{}@{}:{}".format(
                    source.get('username'),
                    source.get('host'),
                    sourcePath
                ),
                destinationPath
            ]
        else:
            raise ValueError("Source is not supported: {}".format(source))

        return self.localCommandExecutor.execute(args)

    def copyToRemote(self, sourcePath: str, destination, destinationPath: str):
        if isinstance(destination, (DeploymentConfigData, BackupConfigData)):
            args = [
                "rsync", "-a", "-q", "--delete",
                "-e", "ssh -p {} -o StrictHostKeyChecking=no".format(
                    str(destination.get('port'))
                ),
                sourcePath,
                "{}@{}:{}".format(
                    destination.get('username'),
                    destination.get('host'),
                    destinationPath
                ),
            ]
        else:
            raise ValueError("Destination is not supported: {}".format(destination))

        return self.localCommandExecutor.execute(args)

    def copy(self, sourcePath: str, destinationPath: str):

        args = [
            "rsync", "-a", "-q", "--delete",
            sourcePath,
            destinationPath
        ]

        return self.localCommandExecutor.execute(args)

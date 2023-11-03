import logging
from wesync.services.config.sections.deploymentConfig import DeploymentConfigData
from wesync.services.config.configManager import ConfigManager
from wesync.services.execute.remoteCommandExecutor import RemoteCommandExecutor


class RemoteProjectCommandExecutor(RemoteCommandExecutor):

    sshBinary = "ssh"

    def __init__(self, config: ConfigManager, deployment: DeploymentConfigData):
        super().__init__(config)
        self.deployment = deployment

    def _getSSHCommands(self) -> list:
        sshArgs = [
            self.sshBinary, "-A",
            "-p", str(self.deployment.get('port')),
            "-l", self.deployment.get('username'),
            "-o", "StrictHostKeyChecking=no",
            self.deployment.get('host')
        ]

        return sshArgs

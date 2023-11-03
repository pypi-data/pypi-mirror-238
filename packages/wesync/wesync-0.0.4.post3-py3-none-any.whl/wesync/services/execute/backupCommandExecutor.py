import logging
from wesync.services.config.sections.backupConfig import BackupConfigData
from wesync.services.config.configManager import ConfigManager
from wesync.services.execute.remoteCommandExecutor import RemoteCommandExecutor


class BackupCommandExecutor(RemoteCommandExecutor):

    def __init__(self, config: ConfigManager, backup: BackupConfigData):
        super().__init__(config)
        self.backup = backup

    def _getSSHCommands(self) -> list:
        sshArgs = [
            self.sshBinary, "-A",
            "-p", str(self.backup.get('port')),
            "-l", self.backup.get('username'),
            "-o", "StrictHostKeyChecking=no",
            self.backup.get('host')
        ]

        return sshArgs

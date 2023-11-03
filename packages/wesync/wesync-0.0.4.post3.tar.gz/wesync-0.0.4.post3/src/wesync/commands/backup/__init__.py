from .backupCommand import BackupCommand
from .backupPush import BackupPushOperation
from .backupPull import BackupPullOperation
from .backupList import BackupListOperation
from .backupExport import BackupExportOperation
from .backupImport import BackupImportOperation

BackupCommand.availableOperations = [
    BackupPushOperation,
    BackupPullOperation,
    BackupListOperation,
    BackupExportOperation,
    BackupImportOperation
]


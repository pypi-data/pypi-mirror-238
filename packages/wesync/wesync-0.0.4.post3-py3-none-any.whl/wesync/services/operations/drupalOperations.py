import logging
from wesync.services.operations.projectOperations import ProjectOperationsService
from wesync.services.snapshot import Snapshot


class DrupalOperationsService(ProjectOperationsService):

    projectType = 'drupal'

    drush = None
    baseCommand = []

    defaultFilePathArtifacts = [{
        "name": "files.tar.gz",
        "path": "web/sites/default/files"
    }]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def detectDrush(self):

        if drush := self.deployment.get('drush'):
            self.drush = drush

        if not self.drush:
            for testBinary in ["drush"]:
                if self.commandAvailable(testBinary):
                    self.drush = testBinary
                    self.deployment.set('drush', self.drush)
                    break

        if not self.drush:
            path = self.deployment.getPath() + "/vendor/drush/drush/drush"
            if self.pathExists(path):
                self.drush = path
                self.deployment.set('drush', self.drush)

        if self.drush:
            self.baseCommand = [self.drush, "--yes", "--root={}".format(self.deployment.get('path'))]
        else:
            raise RuntimeError("Failed to find drush command")

    def fullExport(self, snapshot: Snapshot):
        if self.config.get('only-database') is True:
            self.exportDatabaseToFile(snapshot.getPath('database.sql'))
        else:
            self.exportDatabaseToFile(snapshot.getPath('database.sql'))
            self.exportFileArtifacts(snapshot)

    def fullImport(self, snapshot: Snapshot):
        if self.config.get('only-database') is True:
            self.importDatabaseFromFile(snapshot.getPath('database.sql'))
        else:
            self.importFileArtifacts(snapshot)
            self.importDatabaseFromFile(snapshot.getPath('database.sql'))

    def exportDatabaseToFile(self, databaseExportFile):
        logging.info("Dumping Drupal database at {} to {}".format(self.deployment.getPath(), databaseExportFile))
        args = ["sql:dump", "--result-file={}".format(databaseExportFile),
                "--extra-dump=\"--add-drop-table --no-tablespaces --single-transaction=false\"",
                "--debug"]
        self.runDrush(args, shell=True)

    def importDatabaseFromFile(self, databaseImportFile):
        logging.info("Importing Drupal database at {} to {}".format(databaseImportFile, self.deployment.getPath()))
        args = ["sql:cli < {}".format(databaseImportFile)]
        self.runDrush(args, shell=True)

    def exportDatabaseToStdout(self, **kwargs):
        args = ["-Dssh.tty=0", "sql:dump",
                "--extra-dump=--add-drop-table --no-tablespaces --single-transaction=false"
                ]
        return self.runDrush(args, **kwargs)

    def importDatabaseFromStdin(self, **kwargs):
        args = ["sql:cli"]
        return self.runDrush(args, **kwargs)

    def runDrush(self, args: list, **kwargs):
        if not self.baseCommand:
            self.detectDrush()
        return self.runCommand(self.baseCommand + args, **kwargs)

from wesync.commands.commandManager import CommandWithOperations
from argparse import ArgumentParser


class BackupCommand(CommandWithOperations):

    commandName = 'backup'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def run(self, **kwargs):
        super().run(**kwargs)

    @staticmethod
    def configureArguments(argumentParser: ArgumentParser):
        argumentParser.add_argument("--project", help="Project to lookup in config")

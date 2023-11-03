import logging
from wesync.services.config.configManager import ConfigManager


class CommonOperationsService:

    def __init__(self, config: ConfigManager, executor):
        self.config = config
        self.executor = executor

    def runCommand(self, args, **kwargs):
        if self.config.dryRun() is True:
            logging.info("Dry run: {} ({})".format(args, kwargs))
            return

        if kwargs.get('returnExecutorArgs') is True:
            return self.executor.getArgs(args)

        return self.executor.execute(args, **kwargs)

    def deletePath(self, path, recursive=False, force=False, ignoreErrors=False):
        args = ["rm"]
        if recursive is True:
            args += ["-r"]
        if force is True:
            args += ["-f"]
        args += [path]
        if ignoreErrors is True:
            self.runCommand(args, ignoreRC=True)
        else:
            self.runCommand(args)

    def copyPath(self, fromPath, toPath, recursive=False, ignoreErrors=False):
        args = ["cp"]
        if recursive is True:
            args += ["-r"]
        args += [fromPath, toPath]
        if ignoreErrors is True:
            self.runCommand(args, ignoreRC=True)
        else:
            self.runCommand(args)

    def createPath(self, path):
        args = ["mkdir", "-p", "-v", path]
        self.runCommand(args)

    def commandAvailable(self, command) -> bool:
        processResult = self.runCommand(["which", command], ignoreRC=True)
        return processResult.returncode == 0

    def pathExists(self, path: str, **kwargs) -> bool:
        processResult = self.runCommand(['ls', path], ignoreRC=True, **kwargs)
        return processResult.returncode == 0

    def archiveFiles(self, rootPath: str, files: list, outputArchiveFile: str, **kwargs):
        logging.info("Archiving files at {}/{} to {}".format(rootPath, ','.join(files), outputArchiveFile))
        args = ["tar", "-czpf", outputArchiveFile, '-C', rootPath] + files
        return self.runCommand(args, **kwargs)

    def unarchiveFiles(self, inputArchiveFile, rootPath: str, files: list, delete=False, **kwargs):
        logging.info("Decompressing files at {} to {}/{}".format(inputArchiveFile, rootPath, ','.join(files)))

        if delete is True:
            for file in files:
                deletePath = '/'.join([rootPath, file])
                logging.debug("Removing files at {}".format(deletePath))
                self.deletePath(deletePath, recursive=True, ignoreErrors=True)

        args = ["tar", "-xzpf", inputArchiveFile, '-C', rootPath] + files
        return self.runCommand(args, **kwargs)

    def mktemp(self) -> str:
        processResult = self.runCommand(['mktemp'])
        return processResult.stdout.decode().strip()

    def listDir(self, path) -> list:
        fileListResult = self.runCommand(['ls', '-1', path])
        return fileListResult.stdout.decode().splitlines()

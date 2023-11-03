import logging
import os
import re

import yaml
from wesync.services.config.sections.projectConfig import ProjectConfigData
from wesync.services.config.sections.deploymentConfig import DeploymentConfigData
from wesync.services.config.sections.processorConfig import ProcessorConfigData
from wesync.services.config.sections.backupConfig import BackupConfigData
from wesync.services.config.sections.projectBackupConfig import ProjectBackupConfigData

from .localConfig import LocalConfigData


class LocalConfigManager:

    def __init__(self, configDirectory):
        self.configDirectory = configDirectory

    @staticmethod
    def _getfileLocation() -> str:
        configFileLocation = os.path.expanduser("~/wesync/config/")
        if os.path.exists(".wlkconfig.ini"):
            configFileLocation = ".wlkconfig.ini"
        elif os.path.exists(os.path.expanduser("~/.wlkconfig.ini")):
            configFileLocation = os.path.expanduser("~/.wlkconfig.ini")
        return configFileLocation

    def loadConfig(self) -> LocalConfigData:
        localConfigData = LocalConfigData()

        if not self.hasConfig():
            return localConfigData

        backupPath = self.configDirectory + "/backups"
        if os.path.exists(backupPath):
            backupFiles = os.listdir(backupPath)
        else:
            backupFiles = []

        for backup in backupFiles:
            if re.match(r'.*\.ya?ml$', backup):
                with open(backupPath + "/" + backup, "r") as fd:
                    backupConfigList = yaml.safe_load(fd)

                for backupConfigDict in backupConfigList:
                    backup = BackupConfigData()
                    backup.loadFromConfig(backupConfigDict)
                    localConfigData.registerBackup(backup)

        projectPath = self.configDirectory + "/projects"
        if os.path.exists(projectPath):
            projectFiles = os.listdir(projectPath)
        else:
            projectFiles = []

        for project in projectFiles:

            if re.match(r'.*\.ya?ml$', project):
                with open(projectPath + "/" + project, "r") as fd:
                    projectConfigDict = yaml.safe_load(fd)

                project = ProjectConfigData()
                project.loadFromConfig(projectConfigDict)
                localConfigData.registerProject(project)

                for deploymentConfigDict in projectConfigDict.get('deployments', []):
                    deployment = DeploymentConfigData(project)
                    deployment.loadFromConfig(deploymentConfigDict)
                    localConfigData.registerDeployment(deployment)

                    for processorTriggerName, processorTriggerData in deploymentConfigDict.get('processors', {}).items():
                        for processorConfigDict in processorTriggerData:
                            processor = ProcessorConfigData(processorTriggerName, deployment=deployment)
                            processor.loadFromConfig(processorConfigDict)
                            deployment.addProcessor(processor)

                for processorTriggerName, processorTriggerData in projectConfigDict.get('processors', {}).items():
                    for processorConfigDict in processorTriggerData:
                        processor = ProcessorConfigData(processorTriggerName, project=project)
                        processor.loadFromConfig(processorConfigDict)
                        project.addProcessor(processor)

                for backupProjectConfigDict in projectConfigDict.get('backups', []):
                    projectBackup = ProjectBackupConfigData(project=project)
                    projectBackup.loadFromConfig(backupProjectConfigDict)
                    project.backups.append(projectBackup)

        localConfigData.defaults = {}
        return localConfigData

    def hasConfig(self) -> bool:
        if not os.path.exists(self.configDirectory):
            return False
        if len(os.listdir(self.configDirectory)) == 0:
            return False

        return True

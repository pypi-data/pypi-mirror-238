from wesync.services.operations.drupalOperations import DrupalOperationsService
from wesync.services.operations.wordpressOperations import WordpressOperationsService
from wesync.services.config.sections.deploymentConfig import DeploymentConfigData
from wesync.services.config.configManager import ConfigManager
from collections import defaultdict


class ProjectManagerFactory:
    managers = defaultdict(lambda: {})

    def __int__(self):
        pass

    @classmethod
    def registerProjectManager(cls, projectManager):
        pass

    @classmethod
    def getProjectManagerFor(cls, deployment: DeploymentConfigData, config: ConfigManager, rebuild: bool = False):
        project = deployment.getProject()
        projectType = project.getType()
        projectName = project.getName()
        deploymentName = deployment.getName()

        if manager := cls.managers.get(projectName, {}).get(deploymentName) and rebuild is False:
            return manager

        if projectType == 'drupal':
            manager = DrupalOperationsService(config=config, deployment=deployment)
        elif projectType == 'wordpress':
            manager = WordpressOperationsService(config=config, deployment=deployment)
        else:
            manager = None

        cls.managers[projectName][projectType] = manager

        if manager:
            return manager
        else:
            raise ModuleNotFoundError("Could not find manager to handle {} project type".format(projectType))

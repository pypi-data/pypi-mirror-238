from .terminal import bcolors


class UserInteraction:
    def __init__(self):
        pass

    @staticmethod
    def getColorForLevel(level: str):
        if level == 'info':
            return bcolors.OKCYAN
        if level == 'success':
            return bcolors.OKGREEN
        if level == 'warn':
            return bcolors.WARNING
        if level == 'fail':
            return bcolors.FAIL
        return bcolors.OKBLUE

    @staticmethod
    def print(*args, **kwargs):
        print(UserInteraction.sprint(*args, **kwargs))

    @staticmethod
    def sprint(message: str, level: str = 'info'):
        startColor = UserInteraction.getColorForLevel(level)
        return startColor + message + bcolors.ENDC

    @staticmethod
    def askForAnswer(prompt: str, default=None, allowEmpty=False, level='info'):
        while True:
            if default is None:
                value = input(UserInteraction.sprint("{}: ".format(prompt), level))
            else:
                value = input(UserInteraction.sprint("{} [{}]: ".format(prompt, default), level)) or default

            if value:
                return value

            if allowEmpty is True:
                return value

            else:
                UserInteraction.sprint("Invalid input for previous prompt\n", 'warn')

    @staticmethod
    def confirm(prompt: str = "Continue operation ?", default=False, level="info"):
        if default is True:
            choices = "Y/n"
        elif default is False:
            choices = "y/N"
        else:
            choices = "y/n"

        while True:
            try:
                value = input(UserInteraction.sprint("{} {}: ".format(prompt, choices), level))
                if value in ["n", "N"]:
                    return False
                elif value in ["y", "Y"]:
                    return True
                elif not value:
                    if default is not None:
                        return default
                else:
                    UserInteraction.sprint("Invalid input for previous prompt\n", 'warn')

            except KeyboardInterrupt:
                return False
import os
from configparser import ConfigParser
from enum import Enum
from typing import Optional


class ConfigVariable(Enum):
    """
    Represents a "known" variable that the Cortex SDK cares about.
    """
    API_KEY = 'NH_API_KEY'
    API_URL = 'NH_API_URL'
    PROFILE = 'NH_PROFILE'

class Config():
    """
    Helper for dealing with Cortex configuration and variables.
    """
    NH_PROFILE_PATH = '~/.nearlyhuman/config'

    @staticmethod
    def _get_var_from_env(var: ConfigVariable) -> str | None:
        """
        Try to get a Cortex CLI variable from the environment.
        """
        return os.environ.get(str(var))

    @staticmethod
    def _get_var_from_config(var: ConfigVariable, profile: str) -> str | None:
        """
        Try to get a Cortex CLI variable from the configuration file.
        """
        path = os.path.expanduser(Config.NH_PROFILE_PATH)

        # Just need to care if it exists or not, anything else is probably
        # actually exceptional and should bubble up as a failure
        if not os.path.exists(path):
            return None

        # Config saves variable names in a different format:
        # "NH_API_KEY" -> "api_key"
        parser = ConfigParser()
        parser.read(path)
        return parser[profile].get(var.name.lower())


    @staticmethod
    def get_variable(var: ConfigVariable, profile: str = 'default') -> Optional[str]:
        """
        Try to get a configuration variable based on the specified profile.

        This will attempt to grab a variable, in order of:
        - Environment variable
        - Configuration file

        If the 'prefer' parameter is truthy, that value will always be returned
        This allows for a CLI switch to always win out over other options.
        """
        assert var

        # Return the first available variable
        methods = [
            (Config._get_var_from_env, {'var': var}),
            (Config._get_var_from_config, {'var': var, 'profile': profile})
        ]

        value = None
        for func in methods:
            kargs = func[1]
            value = func[0](**kargs)
            if value:
                return value

        # All attempts to find the variable have failed
        return None

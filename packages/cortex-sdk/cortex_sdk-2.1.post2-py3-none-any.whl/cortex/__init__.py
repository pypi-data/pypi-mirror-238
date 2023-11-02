"""
Cortex API client library.
"""

from cortex.api import (
    Inferences, # noqa: F401
    Models,     # noqa: F401
    Pipelines,  # noqa: F401
    Repos,      # noqa: F401
    Secrets,    # noqa: F401 
    Steps,      # noqa: F401
    Users       # noqa: F401
)

__version__ = '2.1-r2'

from .configuration import Config, ConfigVariable

profile = Config.get_variable(ConfigVariable.PROFILE) or 'default'
api_key = Config.get_variable(ConfigVariable.API_KEY, profile)
api_url = Config.get_variable(ConfigVariable.API_URL, profile)

if api_key is None or api_url is None:
    raise Exception('No Cortex credentials found.')

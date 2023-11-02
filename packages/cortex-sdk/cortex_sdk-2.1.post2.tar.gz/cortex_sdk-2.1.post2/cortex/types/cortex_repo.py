from .cortex_base_type import CortexBaseType


class CortexRepo(CortexBaseType):
    """
    Object representing a Cortex repo returned by the API.
    """

    def __init__(
        self,
        name:         str,
        organization: str,
        description:  str,
        repo:         str
    ): 
        self.name         = name
        self.organization = organization
        self.descriptiion = description
        self.repo         = repo

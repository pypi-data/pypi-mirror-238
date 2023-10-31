from typing import List, Optional
from .cortex_base_type import CortexBaseType


class CortexModel(CortexBaseType):
    """
    Object representing a Cortex model returned by the API.
    """

    def __init__(
        self,
        _id:             str,
        name:            str,
        repo:            str,
        organization:    str,
        updatedDate:     str,
        createdDate:     str,
        tags:            List[str],
        clientKey:       str,
        experimentId:    str,
        memoryRequested: Optional[int] = None,
        memoryEstimate:  Optional[int] = None,
        description:     Optional[str] = None,
        githubEnabled:   Optional[bool] = None,
    ): 
        self.id               = _id
        self.name             = name
        self.repo             = repo
        self.organization     = organization
        self.updated_date     = updatedDate
        self.created_date     = createdDate
        self.tags             = tags
        self.client_key       = clientKey
        self.experiment_id    = experimentId
        self.memory_requested = memoryRequested
        self.memory_estimate  = memoryEstimate
        self.description      = description
        self.github_enabled   = githubEnabled

from typing import Dict, Any, Optional
from .cortex_base_type import CortexBaseType


class CortexStep(CortexBaseType):
    """
    Object representing a Cortex step returned by the API.
    """

    def __init__(
        self,
        _id:            str,
        clientKey:      str,
        pipelineId:     str,
        name:           str,
        type:           str,
        config:         Dict[str, Any],
        order:          int,
        status:         str,
        createdDate:    str,
        updatedDate:    str,
        duration:       Optional[str] = None,
        completionDate: Optional[str] = None,
        statusMessage:  Optional[str] = None,
        risk:           Optional[str] = None,
        runningDate:    Optional[str] = None,
    ):
        self.id              = _id
        self.client_key      = clientKey
        self.pipeline_id     = pipelineId
        self.name            = name
        self.type            = type  # Hopefully this overlap isn't a problem
        self.config          = config
        self.order           = order
        self.status          = status
        self.created_date    = createdDate
        self.updated_date    = updatedDate
        self.completion_date = completionDate
        self.status_message  = statusMessage
        self.risk            = risk
        self.runningDate     = runningDate

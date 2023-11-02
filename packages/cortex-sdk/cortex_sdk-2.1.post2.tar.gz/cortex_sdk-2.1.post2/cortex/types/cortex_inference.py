from typing import List, Dict, Any, Optional
from .cortex_base_type import CortexBaseType


class CortexInference(CortexBaseType):
    """
    Object representing a Cortex inference returned by the API.
    """

    def __init__(
        self,
        _id:              str,
        clientKey:        str,
        modelId:          str,
        pipelineId:       str,
        message:          str,
        successful:       bool,
        createdDate:      str,
        updatedDate:      str,
        duration:         Optional[int] = None,
        inputs:           Optional[List[Dict[str, Any]]] = None,
        inputParameters:  Optional[Dict[str, Any]] = None,
        outputs:          Optional[List[Dict[str, Any]]] = None,
        outputParameters: Optional[Dict[str, Any]] = None,
        threadId:         Optional[str] = None,
        experimentId:     Optional[str] = None,
        currentStage:     Optional[str] = None,
        deploymentStage:  Optional[str] = None,
        deploymentStatus: Optional[str] = None,
        tags:             Optional[List[Dict[str, Any]]] = None,
        annotation:       Optional[str] = None,
        ipAddress:        Optional[str] = None,
        email:            Optional[str] = None,
        parameters:       Optional[str] = None,
    ):
        self.id                = _id
        self.client_key        = clientKey
        self.model_id          = modelId
        self.pipeline_id       = pipelineId
        self.message           = message
        self.successful        = successful
        self.duration          = duration
        self.created_date      = createdDate
        self.updated_date      = updatedDate
        self.inputs            = inputs
        self.input_parameters  = inputParameters
        self.outputs           = outputs
        self.output_parameters = outputParameters
        self.thread_id         = threadId
        self.experiment_id     = experimentId
        self.current_stage     = currentStage
        self.deployment_stage  = deploymentStage
        self.deployment_status = deploymentStatus
        self.tags              = tags
        self.annotation        = annotation
        self.ip_address        = ipAddress
        self.email             = email
        self.parameters        = parameters

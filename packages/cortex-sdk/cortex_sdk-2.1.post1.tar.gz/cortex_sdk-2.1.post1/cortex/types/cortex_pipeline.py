from typing import List, Optional
from .cortex_base_type import CortexBaseType


class CortexPipeline(CortexBaseType):
    """
    Object representing a Cortex pipeline returned by the API.
    """

    def __init__(
        self,
        _id:                  str,
        modelId:              str,
        updatedDate:          str,
        createdDate:          str,
        clientKey:            str,
        deploymentStatus:     bool,
        local:                bool,
        experimentId:         str,
        currentStage:         str,
        pendingDate:          str,
        runId:                str,
        gitBranch:            Optional[str] = None,
        gitHash:              Optional[str] = None,
        cloud:                Optional[bool] = None,
        memoryRequested:      Optional[int] = None,
        memoryEstimate:       Optional[str] = None,
        deploymentStage:      Optional[str] = None,
        runningDate:          Optional[str] = None,
        completionDate:       Optional[str] = None,
        secrets:              Optional[List[str]] = None,
        instanceType:         Optional[str] = None,
        lastDeploymentDate:   Optional[str] = None,
        inferenceURL:         Optional[str] = None,
        lastUndeploymentDate: Optional[str] = None,
        trainingInstance:     Optional[str] = None,
        trainingDuration:     Optional[str] = None,
        lastDeploymentInstance: Optional[str] = None,
        undeploymentDuration: Optional[str] = None,
        tags:                 Optional[List[str]] = None,
    ):
        self.id                = _id
        self.model_id          = modelId
        self.instance_type     = instanceType
        self.git_branch        = gitBranch
        self.cloud             = cloud
        self.updated_date      = updatedDate
        self.created_date      = createdDate
        self.client_key        = clientKey
        self.deployment_status = deploymentStatus
        self.local             = local
        self.memory_requested  = memoryRequested
        self.git_hash          = gitHash
        self.experiment_id     = experimentId
        self.current_stage     = currentStage
        self.pending_date      = pendingDate
        self.run_id            = runId

from typing import List, Optional
from .api_resource import APIResource
from ..types.cortex_step import CortexStep

class Steps(APIResource):
    """
    Cortex Steps API.
    """
    @classmethod
    def get(
        cls, 
        resource_id: Optional[str] = None
    ) -> CortexStep | List[CortexStep]:
        """
        Gets one or many users.

        Args:
            resource_id (str, optional):
            The ID of the step to retrieve. If None, retrieves all steps.

        Returns:
            CortexStep or list[CortexStep]: 
            If resource_id is provided, returns a single CortexStep object.
            If resource_id is None, returns a list of CortexStep objects.
        """
        return cls._generic_get(
            path        = f'/steps/{resource_id or ""}',
            return_type = CortexStep
        )

    @classmethod
    def complete(
        cls, 
        step_id:     str,
        pipeline_id: str,
        name:        str,
        type:        str,
        order:       str,
        status:      str,
        message:     Optional[str]
    ):
        """
        Completes a step.

        Args:
            resource_id (str, optional):
            The ID of the step to retrieve. If None, retrieves all steps.

        Returns:
            CortexStep or list[CortexStep]: 
            If resource_id is provided, returns a single CortexStep object.
            If resource_id is None, returns a list of CortexStep objects.
        """
        return cls._generic_put(
            path = f'/steps/{step_id}/complete',
            json = {
                'pipelineId':    pipeline_id,
                'name':          name,
                'type':          type,
                'order':         order,
                'status':        status,
                'statusMessage': message
            }
        )
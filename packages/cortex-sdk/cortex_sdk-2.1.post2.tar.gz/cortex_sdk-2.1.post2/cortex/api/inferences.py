from typing                   import List, Optional
from .api_resource            import APIResource
from ..types.cortex_inference import CortexInference

class Inferences(APIResource):
    """
    Cortex Inferences API.
    """
    @classmethod
    def get(
        cls,
        resource_id: Optional[str] = None
    ) -> CortexInference | List[CortexInference]:
        """
        Gets one or many inferences.

        Args:
            resource_id (str, optional):
            The ID of the inference to retrieve. If None, retrieves all
            inferences.

        Returns:
            CortexInference or list[CortexInference]: 
            If resource_id is provided, returns a single CortexInference object.
            If resource_id is None, returns a list of CortexInference objects.
        """
        return cls._generic_get(
            path        = f'/inferences/{resource_id or ""}',
            return_type = CortexInference
        )

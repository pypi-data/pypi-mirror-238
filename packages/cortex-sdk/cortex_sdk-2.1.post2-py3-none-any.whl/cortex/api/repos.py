from typing import List, Optional
from .api_resource import APIResource
from ..types.cortex_repo import CortexRepo

class Repos(APIResource):
    """
    Cortex Repos API.
    """
    @classmethod
    def get(
        cls, 
        resource_id: Optional[str] = None
    ) -> CortexRepo| List[CortexRepo]:
        """
        Gets one or many users.

        Args:
            resource_id (str, optional):
            The ID of the repo to retrieve. If None, retrieves all repo.

        Returns:
            CortexRepo or list[CortexRepo]: 
            If resource_id is provided, returns a single CortexRepo object.
            If resource_id is None, returns a list of CortexRepo objects.
        """
        return cls._generic_get(
            path        = f'/repos/{resource_id or ""}',
            return_type = CortexRepo
        )

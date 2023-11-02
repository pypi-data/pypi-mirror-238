from typing import List, Optional
from .api_resource import APIResource
from ..types.cortex_secret import CortexSecret

class Secrets(APIResource):
    """
    Cortex Secrets API.
    """
    @classmethod
    def get(
        cls, 
        resource_id: Optional[str] = None
    ) -> CortexSecret | List[CortexSecret]:
        """
        Gets one or many users.

        Args:
            resource_id (str, optional):
            The ID of the secret to retrieve. If None, retrieves all secrets.

        Returns:
            CortexSecret or list[CortexSecret]: 
            If resource_id is provided, returns a single CortexSecret object.
            If resource_id is None, returns a list of CortexSecret objects.
        """
        return cls._generic_get(
            path        = f'/secrets/{resource_id or ""}',
            return_type = CortexSecret
        )

    @classmethod
    def update(
        cls,
        name:  str,
        value: str
    ):
        """
        THIS IS BUGGED ON THE API SIDE, FIX.
        Updates a secret.

        Args:
            name (str): 
            The name of the secret.

            value (str):
            The value of the secret.
        """
        raise NotImplementedError()
    
    @classmethod
    def create(
        cls,
        name:  str,
        value: str
    ):
        """
        Creates a new secret.

        Args:
            name (str): 
            The name of the secret.

            value (str):
            The value of the secret.
        """
        return cls._generic_post(path='/secrets', json={
            'friendlyName': name,
            'value':        value
        })
    
    @classmethod
    def delete(
        cls,
        resource_id: str
    ):
        """
        Deletes a secret.

        Args:
            resource_id (str): The ID of the secret to delete.
        """
        return cls._generic_delete(path=f'/secrets/{resource_id}')

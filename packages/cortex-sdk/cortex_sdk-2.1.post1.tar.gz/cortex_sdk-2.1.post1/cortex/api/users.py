from typing import List, Optional
from ..types.cortex_user import CortexUser
from .api_resource import APIResource


class Users(APIResource):
    """
    Cortex Users API.
    """

    @classmethod
    def get(
        cls, 
        resource_id: Optional[str] = None
    ) -> CortexUser | List[CortexUser]:
        """
        Gets one or many users.

        Args:
            resource_id (str, optional):
            The ID of the user to retrieve. If None, retrieves all users.

        Returns:
            CortexUser or list[CortexUser]:
            If resource_id is provided, returns a single CortexUser object.
            If resource_id is None, returns a list of CortexUser objects.
        """
        return cls._generic_get(
            path        = f'/users/{resource_id or ""}', 
            return_type = CortexUser
        )

    @classmethod
    def create(
        cls,
        username:     str,
        first_name:   str,
        last_name:    str,
        phone_number: Optional[str]  = None,
        auto_verify:  Optional[bool] = True,
    ):
        """
        Creates a new user.

        Args:
            username (str):
            The username of the user.

            first_name (str):
            The first name of the user.

            last_name (str):
            he last name of the user.

            phone_number (str, optional):
            The phone number of the user.

            auto_verify (bool, optional):
            Whether to automatically verify the user.
        """
        return cls._generic_post(
            path = '/users',
            json = {
                'username':         username,
                'firstName':        first_name,
                'lastName':         last_name,
                'phoneNumber':      phone_number,
                'skipVerification': auto_verify,
            }
        )

    @classmethod
    def delete(
        cls, 
        resource_id: str
    ):
        """
        Deletes a user.

        Args:
            resource_id (str): The ID of the user to delete.
        """
        return cls._generic_delete(path=f'/users/{resource_id}')

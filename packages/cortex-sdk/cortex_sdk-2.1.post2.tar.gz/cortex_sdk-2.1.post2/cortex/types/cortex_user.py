from typing import Optional
from .cortex_base_type import CortexBaseType


class CortexUser(CortexBaseType):
    """
    Object representing a Cortex user returned by the API.
    """

    def __init__(
        self,
        username:             str,
        status:               str,
        creationDate:         int,
        termsOfUseVersion:    Optional[str] = None,
        privacyPolicyVersion: Optional[str] = None,
        firstName:            Optional[str] = None,
        lastName:             Optional[str] = None,
    ): 
        self.id                     = username  # The API doesn't return an _id field
        self.username               = username
        self.first_name             = firstName
        self.given_name             = lastName
        self.status                 = status
        self.creation_date          = creationDate
        self.terms_of_use_version   = termsOfUseVersion
        self.privacy_policy_version = privacyPolicyVersion

from .cortex_base_type import CortexBaseType


class CortexSecret(CortexBaseType): 
    def __init__(
        self,
        _id:          str,
        clientKey:    str,
        friendlyName: str,
        createdDate:  str,
        updatedDate:  str,
    ): 
        self.id           = _id
        self.client_key   = clientKey
        self.name         = friendlyName
        self.created_date = createdDate
        self.updated_date = updatedDate

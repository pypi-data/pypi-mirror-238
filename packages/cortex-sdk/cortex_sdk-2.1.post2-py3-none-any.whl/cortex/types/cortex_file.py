from .cortex_base_type import CortexBaseType


class CortexFile(CortexBaseType):
    """
    Object representing a Cortex file returned by the API.
    """

    def __init__(
        self,
        key:          str,
        name:         str,
        parentPath:   str,
        parent:       str,
        size:         int,
        etag:         str,
        lastModified: str,
    ):
        self.key           = key
        self.name          = name
        self.parent_path   = parentPath
        self.parent        = parent
        self.size          = size
        self.etag          = etag
        self.last_modified = lastModified

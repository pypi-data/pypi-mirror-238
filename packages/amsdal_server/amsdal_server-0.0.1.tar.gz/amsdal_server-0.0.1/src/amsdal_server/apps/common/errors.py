from amsdal_utils.errors import AmsdalError

from amsdal_server.apps.common.permissions.enums import AccessTypes


class AmsdalPermissionError(AmsdalError):
    def __init__(self, access_type: AccessTypes, class_name: str) -> None:
        self.access_type = access_type
        self.class_name = class_name

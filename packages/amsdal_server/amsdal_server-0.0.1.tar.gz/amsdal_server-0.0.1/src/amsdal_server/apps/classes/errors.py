from typing import Any

from amsdal_utils.errors import AmsdalError


class ClassNotFoundError(AmsdalError):
    def __init__(self, class_name: str, *args: Any) -> None:
        self.class_name = class_name
        super().__init__(*args)

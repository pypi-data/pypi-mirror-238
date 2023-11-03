from typing import Any

from pydantic import BaseModel

from amsdal_server.apps.common.serializers.column_response import ColumnInfo


class ObjectsResponse(BaseModel):
    columns: list[ColumnInfo]
    rows: list[Any]

from pydantic import BaseModel
from pydantic import Field


class ColumnFormat(BaseModel):
    header_template: str | None = Field(None, alias='headerTemplate')
    cell_template: str | None = Field(None, alias='cellTemplate')

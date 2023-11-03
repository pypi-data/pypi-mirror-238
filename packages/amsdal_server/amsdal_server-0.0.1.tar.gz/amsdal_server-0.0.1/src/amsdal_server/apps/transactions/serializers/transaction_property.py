from pydantic import BaseModel


class TypeSerializer(BaseModel):
    type: str  # noqa: A003


class DictTypeSerializer(BaseModel):
    key: TypeSerializer
    value: TypeSerializer


class TransactionPropertySerializer(BaseModel):
    title: str
    type: str = 'string'  # noqa: A003
    items: DictTypeSerializer | TypeSerializer | None = None

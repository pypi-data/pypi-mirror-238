import ast
from collections.abc import Generator
from pathlib import Path

from amsdal_framework.configs.main import settings
from amsdal_models.schemas.enums import CoreTypes

from amsdal_server.apps.transactions.serializers.transaction_item import TransactionItemSerializer
from amsdal_server.apps.transactions.serializers.transaction_property import DictTypeSerializer
from amsdal_server.apps.transactions.serializers.transaction_property import TransactionPropertySerializer
from amsdal_server.apps.transactions.serializers.transaction_property import TypeSerializer
from amsdal_server.apps.transactions.utils import is_transaction


class AstParserMixin:
    @classmethod
    def _get_transaction_definitions(cls) -> Generator[ast.FunctionDef | ast.AsyncFunctionDef, None, None]:
        transactions_path: Path = cls._get_transactions_path()

        if not transactions_path.exists():
            return

        transactions_content = Path(transactions_path).read_text()
        tree = ast.parse(transactions_content)

        for definition in ast.walk(tree):
            if not is_transaction(definition):
                continue

            yield definition  # type: ignore[misc]

    @classmethod
    def build_transaction_item(cls, definition: ast.FunctionDef | ast.AsyncFunctionDef) -> TransactionItemSerializer:
        transaction_item = TransactionItemSerializer(
            title=definition.name,
            properties={},
        )

        for arg in definition.args.args:
            if hasattr(arg.annotation, 'id'):
                transaction_item.properties[arg.arg] = TransactionPropertySerializer(
                    title=arg.arg,
                    type=cls._normalize_type(arg.annotation.id),  # type: ignore[union-attr]
                )
            elif hasattr(arg.annotation, 'value'):
                if arg.annotation.value.id.lower() == 'list':  # type: ignore[union-attr]
                    transaction_item.properties[arg.arg] = TransactionPropertySerializer(
                        title=arg.arg,
                        type=CoreTypes.ARRAY.value,
                        items=TypeSerializer(
                            type=cls._normalize_type(arg.annotation.slice.id),  # type: ignore[union-attr]
                        ),
                    )
                elif arg.annotation.value.id.lower() == 'dict':  # type: ignore[union-attr]
                    transaction_item.properties[arg.arg] = TransactionPropertySerializer(
                        title=arg.arg,
                        type=CoreTypes.ARRAY.value,
                        items=DictTypeSerializer(
                            key=TypeSerializer(
                                type=cls._normalize_type(arg.annotation.slice.elts[0].id),  # type: ignore[union-attr]
                            ),
                            value=TypeSerializer(
                                type=cls._normalize_type(arg.annotation.slice.elts[1].id),  # type: ignore[union-attr]
                            ),
                        ),
                    )
                else:
                    msg = 'Error parsing annotation with value and no id attribute is not expected...'
                    raise ValueError(msg)
            else:
                transaction_item.properties[arg.arg] = TransactionPropertySerializer(
                    title=arg.arg,
                    type=CoreTypes.ANYTHING.value,
                )

        return transaction_item

    @classmethod
    def _get_transactions_path(cls) -> Path:
        return settings.models_root_path / 'transactions.py'

    @classmethod
    def _normalize_type(cls, json_or_py_type: str) -> str:
        json_switcher = {
            CoreTypes.STRING.value: 'str',
            CoreTypes.NUMBER.value: 'float',
            CoreTypes.ANYTHING.value: 'Any',
            CoreTypes.BOOLEAN.value: 'bool',
            CoreTypes.BINARY.value: 'bytes',
            CoreTypes.ARRAY.value: 'List',
        }
        py_switcher = {
            'str': CoreTypes.STRING.value,
            'int': CoreTypes.NUMBER.value,
            'float': CoreTypes.NUMBER.value,
            'Any': CoreTypes.ANYTHING.value,
            'bool': CoreTypes.BOOLEAN.value,
            'bytes': CoreTypes.BINARY.value,
            'List': CoreTypes.ARRAY.value,
        }

        return json_switcher.get(json_or_py_type, py_switcher.get(json_or_py_type, json_or_py_type))

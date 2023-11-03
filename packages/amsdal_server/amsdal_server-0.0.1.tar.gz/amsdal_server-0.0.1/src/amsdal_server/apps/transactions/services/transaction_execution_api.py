from typing import Any

from amsdal_framework.services.transaction_execution import TransactionExecutionService


class TransactionExecutionApi:
    @classmethod
    def execute_transaction(
        cls,
        transaction_name: str,
        args: dict[Any, Any],
    ) -> Any:
        execution_service = TransactionExecutionService()

        return execution_service.execute_transaction(
            transaction_name=transaction_name,
            args=args,
        )

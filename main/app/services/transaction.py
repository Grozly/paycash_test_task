from uuid import UUID
from abc import ABC, abstractmethod
from dataclasses import dataclass

from fastapi import HTTPException

from app import (
    schemas,
    adapters,
    storage,
)


class FrameworkAdapter(ABC):
    """
    Global framework interface adapter.
    """

    @abstractmethod
    def http_exception_400(
        self,
        detail: str,
    ) -> HTTPException:
        ...


class TransactionStorage(ABC):
    """
    Global transaction storage interface adapter.
    """

    @abstractmethod
    async def async_create(
        self,
        transaction_data: schemas.TransactionRequestData,
    ) -> schemas.TransactionResponse:
        ...

    @abstractmethod
    async def async_get_by_uuid(
        self,
        transaction_uuid: UUID,
    ) -> schemas.TransactionResponse:
        ...


@dataclass
class TransactionUseCase:
    """
    Transaction business rules.
    """

    transaction_storage: TransactionStorage = storage.TransactionDBStorage()
    framework_adapter: FrameworkAdapter = adapters.FastapiAdapter()

    async def create_transaction(
        self, transaction_data: schemas.TransactionRequestData
    ) -> schemas.TransactionResponse:
        if not transaction_data:
            raise self.framework_adapter.http_exception_400(
                f"Not found transaction data!"
            )

        transaction = await self.transaction_storage.async_create(transaction_data)

        if not transaction:
            raise self.framework_adapter.http_exception_400(
                f"Don't saved transaction data!"
            )

        return transaction

    async def get_transaction_by_uuid(
        self,
        transaction_uuid: UUID,
    ) -> schemas.TransactionResponse:
        transaction = await self.transaction_storage.async_get_by_uuid(transaction_uuid)

        if not transaction:
            raise self.framework_adapter.http_exception_400(
                f"Not found transaction by uid={transaction_uuid}!"
            )

        return transaction

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


class UserStorage(ABC):
    """
    Global user storage interface adapter.
    """

    @abstractmethod
    async def async_create(
        self,
        user_data: schemas.UserRequest,
    ) -> schemas.UserResponse:
        ...

    @abstractmethod
    async def async_get_by_id(
        self,
        user_id: int,
    ) -> schemas.UserResponse:
        ...

    @abstractmethod
    async def async_get_user_balance_by_id(
        self,
        user_id: int,
    ) -> schemas.UserBalanceResponse:
        ...


@dataclass
class UserUseCase:
    """
    User business rules.
    """

    user_storage: UserStorage = storage.UserDBStorage()
    framework_adapter: FrameworkAdapter = adapters.FastapiAdapter()

    async def create_user(self, user_data: schemas.UserRequest) -> schemas.UserResponse:
        if not user_data:
            raise self.framework_adapter.http_exception_400(f"Not found user data!")

        user = await self.user_storage.async_create(user_data)
        return user

    async def get_user(self, user_id: int) -> schemas.UserResponse:
        user = await self.user_storage.async_get_by_id(user_id)

        if not user:
            raise self.framework_adapter.http_exception_400(
                f"Not found user by id={user_id}!"
            )

        return user

    async def get_user_balance(self, user_id: int) -> schemas.UserBalanceResponse:
        user_balance = await self.user_storage.async_get_user_balance_by_id(user_id)

        if not user_balance:
            raise self.framework_adapter.http_exception_400(
                f"Not found user balance by id={user_id}!"
            )

        return user_balance

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import (
    select,
    insert,
)

from app import schemas, models
from app.config.database import async_session


class UserDBStorage:
    """
    DB connection and query processing class for User model.
    """

    @async_session
    async def async_create(
        self, user_data: schemas.UserRequest, async_session: AsyncSession
    ) -> schemas.UserResponse:
        """
        Create User in DB by user data.

        Args:
            user_data (schemas.UserRequest): instance user data
            async_session (AsyncSession): async session object
        Returns:
            schemas.UserResponse: user response schema object
        """
        user_data_dict = user_data.dict()
        sql_query = insert(models.User).values(**user_data_dict)

        result = await async_session.execute(sql_query)
        await async_session.commit()

        return schemas.UserResponse(id=result.inserted_primary_key.id, **user_data_dict)

    @async_session
    async def async_get_by_id(
        self, user_id: int, async_session: AsyncSession
    ) -> schemas.UserResponse | None:
        """
        Get user from DB by id.

        Args:
            user_id (int): instance user id
            async_session (AsyncSession): async session object
        Returns:
            schemas.UserResponse | None: user response schema object or None
        """
        sql_query = select(models.User).where(models.User.id == user_id)
        result = await async_session.execute(sql_query)

        user_db = result.scalars().one_or_none()
        if not user_db:
            return

        return schemas.UserResponse.from_orm(user_db)

    @async_session
    async def async_get_user_balance_by_id(
        self, user_id: int, async_session: AsyncSession
    ) -> schemas.UserBalanceResponse:
        """
        Get current user balance by user id.
        Args:
            user_id (int): instance user id
            async_session (AsyncSession): async session object
        Returns:
            schemas.UserBalanceResponse | None: user balance response schema object or None
        """
        sql_query = select(models.User).where(models.User.id == user_id)
        result = await async_session.execute(sql_query)

        user_db = result.scalars().one_or_none()
        if not user_db:
            return

        return schemas.UserBalanceResponse(balance=user_db.balance)

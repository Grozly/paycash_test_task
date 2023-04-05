from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import (
    select,
    insert,
    update,
)

from app import (
    schemas,
    models,
)
from app.schemas.transaction import DEPOSIT_TYPE, WITHDRAW_TYPE
from app.config.database import async_session


class TransactionDBStorage:
    """
    DB connection and query processing class for Transaction model.
    """

    async def _update_user_balance(
        self, transaction_data: dict, async_session: AsyncSession
    ) -> int | None:
        """
        Update user balance.

        Args:
            transaction_data (dict): instance transaction data
            async_session (AsyncSession): instance DB async session
        Returns:
            int | None: current User model or None
        """
        user_id = transaction_data["user_id"]
        transaction_type = transaction_data["type"]
        amount = transaction_data["amount"]

        sql_query_select = select(models.User).where(models.User.id == user_id)

        if transaction_type == WITHDRAW_TYPE:
            amount = amount * -1

        result = await async_session.execute(sql_query_select)
        user_db = result.scalars().one_or_none()

        if not user_db:
            return

        total_balance = user_db.balance + amount

        if total_balance < 0:
            return

        sql_query_update = (
            update(models.User)
            .where(models.User.id == user_id)
            .values(balance=total_balance)
        )

        result = await async_session.execute(sql_query_update)
        return user_db.id

    @async_session
    async def async_create(
        self,
        transaction_data: schemas.TransactionRequestData,
        async_session: AsyncSession,
    ) -> schemas.TransactionResponse | None:
        """
        Create Transaction in DB by transaction data.

        Args:
            transaction_data (schemas.TransactionRequestData): instance transaction data
            async_session (AsyncSession): async session object
        Returns:
            schemas.TransactionResponse: transaction schema object
        """
        transaction_data_dict = transaction_data.dict()
        sql_query = insert(models.Transaction).values(**transaction_data_dict)

        result = await async_session.execute(sql_query)
        user_db_id = await self._update_user_balance(
            transaction_data_dict, async_session
        )

        if not user_db_id:
            return

        await async_session.commit()
        return schemas.TransactionResponse(**transaction_data_dict)

    @async_session
    async def async_get_by_uuid(
        self,
        transaction_uuid: str,
        async_session: AsyncSession,
    ) -> schemas.TransactionResponse:
        """
        Get transaction from DB by uuid.

        Args:
            transaction_uuid (UUID): instance transaction UUID
            async_session (AsyncSession): async session object
        Returns:
            schemas.TransactionResponse | None: transaction schema object or None
        """
        sql_query = select(models.Transaction).where(
            models.Transaction.uid == transaction_uuid
        )
        result = await async_session.execute(sql_query)

        transaction_db = result.scalars().one_or_none()
        if not transaction_db:
            return

        return schemas.TransactionResponse.from_orm(transaction_db)

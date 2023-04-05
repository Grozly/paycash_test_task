from uuid import UUID
from typing import Literal
from datetime import datetime

from pydantic import BaseModel, PositiveFloat


DEPOSIT_TYPE = "DEPOSIT"
WITHDRAW_TYPE = "WITHDRAW"


class BaseTransactionSchema(BaseModel):
    uid: UUID | None = None

    class Config:
        orm_mode = True


class TransactionRequest(BaseTransactionSchema):
    pass


class TransactionRequestData(BaseTransactionSchema):
    type: Literal[DEPOSIT_TYPE, WITHDRAW_TYPE]
    amount: PositiveFloat
    user_id: int


class TransactionResponse(BaseTransactionSchema):
    type: str
    amount: PositiveFloat
    user_id: int
    timestamp: datetime | None = None

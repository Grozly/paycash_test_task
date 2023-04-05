import logging

from fastapi import APIRouter, status

from app import (
    schemas,
    services,
)
from app.config.settings import settings


logger = logging.getLogger(settings.LOGGER_NAME)
router = APIRouter()


@router.post(
    "/",
    tags=["transaction"],
    response_model=schemas.TransactionResponse,
    response_model_exclude_none=True,
    status_code=status.HTTP_201_CREATED,
)
async def create_transaction(transaction_data: schemas.TransactionRequestData):
    """
    Create transaction in database.

    Args:
        transaction_data (schemas.TransactionRequestData): transaction data
    Return:
        schemas.TransactionResponse: transaction data response
    """
    use_case = services.TransactionUseCase()
    current_transaction = await use_case.create_transaction(transaction_data)
    logger.info(
        f"Create new transaction - "
        f"id: {current_transaction.uid}, "
        f"type: {current_transaction.type}, "
        f"amount: {current_transaction.amount}, "
        f"user_id: {current_transaction.user_id}"
    )
    return current_transaction


@router.get(
    "/{transaction_uid}",
    tags=["transaction"],
    response_model=schemas.TransactionResponse,
    status_code=status.HTTP_200_OK,
)
async def get_transaction(transaction_uid: str):
    """
    Get transaction by uid.

    Args:
        transaction_uid (int): transaction uid
    Return:
        schemas.TransactionResponse: transaction data response
    """
    use_case = services.TransactionUseCase()
    current_user = await use_case.get_transaction_by_uuid(
        transaction_uuid=transaction_uid
    )
    return current_user

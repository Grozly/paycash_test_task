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
    tags=["user"],
    response_model=schemas.UserResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_user(user_data: schemas.UserRequest):
    """
    Create user in database.

    Args:
        user_data (schemas.UserRequest): user data
    Return:
        schemas.UserResponse: user data response
    """
    use_case = services.UserUseCase()
    current_user = await use_case.create_user(user_data)
    logger.info(
        f"Create new user - "
        f"id: {current_user.id}, "
        f"name: {current_user.name}, "
        f"balance: {current_user.balance}"
    )
    return current_user


@router.get(
    "/{user_id}",
    tags=["user"],
    response_model=schemas.UserResponse,
    status_code=status.HTTP_200_OK,
)
async def get_user(user_id: int):
    """
    Get user by id.

    Args:
        user_id (int): user data
    Return:
        schemas.UserResponse: user data response
    """
    use_case = services.UserUseCase()
    current_user = await use_case.get_user(user_id=user_id)
    return current_user


@router.get(
    "/balance/{user_id}",
    tags=["user"],
    response_model=schemas.UserBalanceResponse,
    status_code=status.HTTP_200_OK,
)
async def get_user_balance(user_id: int):
    """
    Get user balance by id.

    Args:
        user_id (int): user data
    Return:
        schemas.UserBalanceResponse: user data response
    """
    use_case = services.UserUseCase()
    current_user = await use_case.get_user_balance(user_id=user_id)
    return current_user

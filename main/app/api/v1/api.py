from fastapi import APIRouter

from app.api.v1.endpoints import (
    user,
    transaction,
)


api_router = APIRouter()
api_router.include_router(user.router, prefix="/user")
api_router.include_router(transaction.router, prefix="/transaction")

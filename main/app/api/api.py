from fastapi import APIRouter

from app.api.v1 import api as api_v1


api_router = APIRouter()
api_router.include_router(api_v1.api_router, prefix="/v1")

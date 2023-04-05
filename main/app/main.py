import logging
from logging.config import dictConfig

from fastapi import FastAPI

from app import schemas
from app.config.settings import settings
from app.api.api import api_router


dictConfig(schemas.LogConfig().dict())
logger = logging.getLogger(settings.LOGGER_NAME)


app = FastAPI(title="balance_sheets")
app.include_router(api_router, tags=["balance_sheets"])


logger.info("Server started!")

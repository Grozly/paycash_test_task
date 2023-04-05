import pathlib

from pydantic import BaseSettings, PostgresDsn


class Settings(BaseSettings):
    """
    Global project settings.
    """

    # Database
    DB_NAME: str = "paycash"
    DB_USERNAME: str = "paycash_user"
    DB_PASSWORD: str = "paycash"
    DB_HOST: str = "paycash_db"
    DB_PORT: str = "5432"
    DB_URL: PostgresDsn = f"postgresql+asyncpg://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

    # Logs
    LOGGER_NAME: str = "pay_cash"

    # Dirs
    BASE_DIR: pathlib.PosixPath = pathlib.Path(__file__).resolve().parent.parent

    class Config:
        env_file = pathlib.Path(__file__).resolve().parent.parent.joinpath("main.env")
        env_file_encoding = "utf-8"


settings = Settings()

import logging
import pathlib
from functools import lru_cache
from typing import Optional

from pydantic_settings import BaseSettings
#from pydantic import BaseSettings

SCRIPT_PATH = pathlib.Path(__file__).resolve().parent
LOCALES_DIR = SCRIPT_PATH.joinpath('locales')


class Settings(BaseSettings):
    environment: str = ''
    version: str = '0.0.0'
    sqlalchemy_database_uri: str
    secret: str

    class Config:
        env_file = '.env'


@lru_cache()
def get_settings():
    return Settings()

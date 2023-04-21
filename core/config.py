import os
from typing import Optional

from dotenv import load_dotenv
from pydantic import BaseSettings
from pydantic.env_settings import DotenvType

load_dotenv()


class Settings(BaseSettings):
    """FastAPI settings for config project."""

    # Project configuration
    DEBUG: bool = True
    PROJECT_VERSION: str = "1.0.0"
    PROJECT_NAME: str = "temirovazat"
    TITLE: str = "Recipe service"
    DESCRIPTION: str = "This is a simple FastAPI-based web application that allows users to \
    create, view, update, and delete recipes, as well as leave ratings for recipes through the REST API."
    API_V1_STR: str = "/api/v1"

    # Database configuration
    POSTGRES_USER: str = os.getenv("POSTGRES_USER", "postgres")
    POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "postgres")
    POSTGRES_HOST: str = os.getenv("POSTGRES_HOST", "localhost")
    POSTGRES_PORT: str = os.getenv("POSTGRES_PORT", 5432)
    POSTGRES_DB: str = os.getenv("POSTGRES_DB", "postgres")
    DATABASE_URL = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"

    # Test database configuration
    DB_TEST_USER = os.getenv("DB_TEST_USER", "postgres")
    DB_TEST_PASS = os.getenv("DB_TEST_PASS", "postgres")
    DB_TEST_HOST = os.getenv("DB_TEST_HOST", "localhost")
    DB_TEST_PORT = os.getenv("DB_TEST_PORT", 5432)
    DB_TEST_NAME = os.getenv("DB_TEST_NAME", "tests")
    DATABASE_TEST_URL = f"postgresql://{DB_TEST_USER}:{DB_TEST_PASS}@{DB_TEST_HOST}:{DB_TEST_PORT}/{DB_TEST_NAME}"

    class Config:
        env_file: Optional[DotenvType] = "./.env"


settings = Settings()

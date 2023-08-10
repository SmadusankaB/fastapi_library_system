import os
from pathlib import Path

from dotenv import load_dotenv

env_path = Path(".") / ".env"
load_dotenv(dotenv_path=env_path)


class BaseConfig:
    PROJECT: str = "My Library"
    VERSION: str = "1.0.0"
    ALGORITHM = "HS256"
    APP_ACCESS_TOKEN_EXPIRE_MINUTES = 30
    ORIGINS = [
        "http://localhost",
        "http://localhost:8080",
        "http://localhost:8000",
        "http://127.0.0.1:8000",
    ]
    LOGGER_NAME = "app_logger"


class DevelopmentConfig(BaseConfig):
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "DEBUG").upper()
    APP_SECRET_KEY: str = os.getenv("APP_SECRET", "dev_secret")


class ProductionConfig(BaseConfig):
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO").upper()
    APP_SECRET_KEY: str = os.getenv("APP_SECRET", "prod_secret")


class TestingConfig(BaseConfig):
    pass


def get_settings():
    """
    Create correct config class based on value in APP_CONFIG env

    Returns
    -------
    is_correct_file: cls object
        Return DevelopmentConfig,  ProductionConfig or TestingConfig
    """
    config_cls_dict = {
        "development": DevelopmentConfig,
        "production": ProductionConfig,
        "testing": TestingConfig,
    }

    config_name: str = os.getenv("APP_CONFIG", "development")
    config_cls = config_cls_dict[config_name]
    return config_cls()


settings = get_settings()

#
# Copyright (C) 2021
#
# Author: hacktribe <hacktribe.org>
#

import logging
from typing import List, Union

from app.core.logging import InterceptHandler
from loguru import logger
from pydantic import AnyHttpUrl, BaseSettings, IPvAnyAddress


class Settings(BaseSettings):
    project_name: str = "info-leak-monitor"
    allowed_hosts: List[str] = ["*"]
    api_prefix: str = "/api"

    version: str = "0.0.0"
    debug: bool = True

    twepoch: int = 0  # id worker start time

    docs_url: str = f"{api_prefix}/docs"
    openapi_url: str = f"{api_prefix}/openapi.json"
    redoc_url: str = f"{api_prefix}/redoc"

    jwt_token_prefix: str = "settings/tokens"
    algorithm: str = "HS256"
    secret_key: str = "info-leak-monitor_hacktribe"
    access_token_expire: int = 60 * 60 * 24 * 7
    apscheduler_max_instances: int = 10
    log_file: str = "info.log"

    database_username: str = "root"
    database_password: str = ""
    database_host: Union[str, AnyHttpUrl, IPvAnyAddress] = "database"
    database_port: int = 3306
    database_name: str = "info-leak-monitor"
    database_echo: bool = True

    task_modules: List[str] = [
        "app.tasks.default",
        "app.tasks.github",
        "app.tasks.gitlab",
    ]
    task_max_worker: int = 10
    gitlab_repository: str = "https://gitlab.com"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
# logging configuration

LOGGING_LEVEL = logging.DEBUG if settings.debug else logging.ERROR
LOGGERS = ("uvicorn.asgi", "uvicorn.access")

logging.getLogger().handlers = [InterceptHandler()]
for logger_name in LOGGERS:
    logging_logger = logging.getLogger(logger_name)
    logging_logger.handlers = [InterceptHandler(level=LOGGING_LEVEL)]

logger.configure(
    handlers=[{
        "sink": settings.log_file,
        "level": LOGGING_LEVEL,
        "rotation": "00:00",
        "retention": "10 days",
        "format": "{time:YYYY-MM-DD at HH:mm:ss} | {level} | {message}",
    }])

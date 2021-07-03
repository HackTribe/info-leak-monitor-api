#
# Copyright (C) 2021
#
# Author: hacktribe <hacktribe.org>
#

from typing import Callable

from app.core.config import settings
from apscheduler.events import EVENT_JOB_ERROR, EVENT_JOB_EXECUTED
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from fastapi import FastAPI
from loguru import logger
from pytz import utc


def task_listener(event):
    if event.exception:
        logger.error("task id {0} {1}", event.job_id, event.exception)


async def start_scheduler(app: FastAPI) -> None:
    logger.info(
        "APScheduler Starting",
        repr((
            f"mysql+pymysql://{settings.database_username}:{settings.database_password}@"
            f"{settings.database_host}:{settings.database_port}/{settings.database_name}?charset=utf8mb4"
        )),
    )
    jobstores = {
        "default":
        SQLAlchemyJobStore(url=(
            f"mysql+pymysql://{settings.database_username}:{settings.database_password}@"
            f"{settings.database_host}:{settings.database_port}/{settings.database_name}?charset=utf8mb4"
        ))
    }
    job_defaults = {
        "coalesce": False,
        "max_instances": settings.apscheduler_max_instances,
    }
    app.scheduler = AsyncIOScheduler()
    app.scheduler.configure(
        jobstores=jobstores,
        job_defaults=job_defaults,
        # logger=logger,
        timezone=utc,
    )

    app.scheduler.add_listener(task_listener,
                               EVENT_JOB_EXECUTED | EVENT_JOB_ERROR)

    app.scheduler.start()
    logger.info("APScheduler established")


async def stop_scheduler(app: FastAPI) -> None:
    logger.info("APScheduler Closing")

    await app.scheduler.close()

    logger.info("APScheduler closed")


def create_start_app_handler(app: FastAPI) -> Callable:
    async def start_app() -> None:
        await start_scheduler(app)

    return start_app


def create_stop_app_handler(app: FastAPI) -> Callable:
    async def stop_app() -> None:
        await stop_scheduler(app)

    return stop_app

#
# Copyright (C) 2021
#
# Author: hacktribe <hacktribe.org>
#
import importlib
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from typing import Dict, Generator, List
from loguru import logger
from starlette.requests import Request
from app.db.session import SessionLocal
from app.core.config import settings


def get_db() -> Generator:
    db = SessionLocal()
    try:
        yield db
    except Exception:
        db.rollback()
    finally:
        db.close()


def get_scheduler(request: Request) -> AsyncIOScheduler:
    return request.app.scheduler


def get_tasks() -> List[Dict]:
    modules = []
    for task_module_class in settings.task_modules:
        module = importlib.import_module(".", task_module_class)
        do = None
        name = None
        for attr in dir(module):
            if attr[0] != "_":
                obj = getattr(module, attr)
                if hasattr(obj, "__call__") and hasattr(obj, "__name__"):
                    do = obj if obj.__name__ == "do" else do
                    name = obj if obj.__name__ == "name" else name
        if do and name:
            modules.append({"do": do, "name": name})
    return modules

#
# Copyright (C) 2021 hacktribe
#
# Author: hacktribe <hacktribe.org>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
#

from pytz import utc
from datetime import datetime
from typing import List
from concurrent.futures import ThreadPoolExecutor
from loguru import logger
from app.core.config import settings
from app.db.session import SessionLocal
from app.schemas.tasks import TaskInfo
from app.repositories.tokens import TokenRepository
from contextlib import contextmanager

MAX_WORKER = settings.task_max_worker if hasattr(settings,
                                                 "task_max_worker") else 10
PER_SUBMIT_NUM: int = 30
INTERVAL_SECONDS: int = 60


@contextmanager
def session_maker():
    session = SessionLocal()
    try:
        yield session
        # session.commit()
    except Exception:
        session.rollback()
    finally:
        session.close()


def keywords_split(keywords: List[str],
                   per_page: int,
                   start_index: int = 0) -> list:
    """
    Single thread processing multiple keywords, Set every 'N' keywords a Group.
    """
    end_index = start_index + per_page

    if (end_index) > len(keywords):
        return keywords[start_index:len(keywords)]

    return keywords[start_index:end_index]


def submit(executor: ThreadPoolExecutor, doing, job: TaskInfo, pages: int):

    for index in range(0, pages):
        start_index = index
        new_keywords = []
        if index != 0:
            start_index = index * PER_SUBMIT_NUM
        if job.keywords and len(job.keywords) > 0:
            new_keywords = keywords_split(job.keywords, PER_SUBMIT_NUM,
                                          start_index)
        else:
            return

        def callback(f):
            exc, tb = (f.exception_info() if hasattr(f, "exception_info") else
                       (f.exception(),
                        getattr(f.exception(), "__traceback__", None)))
            if exc:
                logger.error("{0} - work failed, exception: {1}", exc, tb)
            else:
                logger.info("{0} - search code done", job.kind)

        logger.debug("submit {} - keywords {}", index, new_keywords)
        executor.submit(doing, job, new_keywords).add_done_callback(callback)


def get_available_token(kind: str) -> str:
    with session_maker() as db:
        _, access_tokens = TokenRepository(db=db).get_token_by_kind(kind)
    for token in access_tokens:
        now = int(datetime.now(utc).timestamp())
        if token.next_time < now:
            return token.access_token
    return ""


def get_reset_token(next_time: int, token: str):
    try:
        with session_maker() as db:
            TokenRepository(db=db).set_next_time_by_access_token(
                token, next_time)
    except Exception as e:
        logger.error("set token <{0}> next_time error: {1}", token, e)

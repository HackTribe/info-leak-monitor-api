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

from typing import Dict, List
import datetime
from loguru import logger

from app.core.deps import get_scheduler, get_tasks
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from fastapi import HTTPException, Depends
from pytz import utc
from starlette.status import HTTP_403_FORBIDDEN
from app.schemas.tasks import TaskInfo, ResponseTaskInfo, UpdateTaskInfo


class TaskService(object):
    job_callbacks = {
        # "github": github.search,
        # "gitlab": gitlab.search,
        # "default": DefaultTask.do
    }
    scheduler: AsyncIOScheduler

    def __init__(
            self,
            scheduler: AsyncIOScheduler = Depends(get_scheduler),
            tasks: List[Dict] = Depends(get_tasks),
    ):
        self.scheduler = scheduler
        for task in tasks:
            self.job_callbacks.update({task.get("name")(): task.get("do")})

    def get_jobs(self) -> List[ResponseTaskInfo]:
        jobs = self.scheduler.get_jobs()
        results = []

        for job in jobs:
            (props, ) = job.args
            if job.next_run_time:
                state = "runing"
            else:
                state = "stop"
            excludes = None
            if hasattr(props, "excludes"):
                excludes = props.excludes
            results.append(
                ResponseTaskInfo(
                    id=job.id,
                    name=job.name,
                    kind=props.kind,
                    state=state,
                    pages=props.pages,
                    keywords=props.keywords,
                    excludes=excludes,
                    runtime_type=props.runtime_type,
                    runtime=props.runtime,
                ))

        return results

    def get_jobs_by_kind(self, kind: str) -> List[ResponseTaskInfo]:
        return [t for t in self.get_jobs() if t.kind == kind]

    def add_job(
        self,
        job: TaskInfo,
    ) -> ResponseTaskInfo:
        if job.kind:
            callback = self.job_callbacks.get(job.kind, None)
        else:
            callback = None
        newjob = None
        if not callback:
            raise HTTPException(
                status_code=HTTP_403_FORBIDDEN,
                detail="'{0}' task not existed.".format(job.kind),
            )

        if job.runtime_type == 1:

            newjob = self.scheduler.add_job(callback,
                                            "interval",
                                            name=job.name,
                                            minutes=job.runtime,
                                            args=(job, ))

        if job.runtime_type == 2:
            newjob = self.scheduler.add_job(
                callback,
                name=job.name,
                args=(job, ),
                trigger=CronTrigger.from_crontab(job.runtime),
            )

        new_job = ResponseTaskInfo(
            kind=job.kind,
            name=job.name,
            runtime_type=job.runtime_type,
            runtime=job.runtime,
            pages=job.pages,
            keywords=job.keywords,
            excludes=job.excludes,
        )
        if newjob:
            new_job.id = newjob.id

        return new_job

    def modify_job(
        self,
        job: UpdateTaskInfo,
    ) -> ResponseTaskInfo:
        if job.kind:
            callback = self.job_callbacks.get(job.kind, None)
        else:
            callback = None
        if not callback or not job.id:
            raise HTTPException(
                status_code=HTTP_403_FORBIDDEN,
                detail="'{0}' task not existed.".format(job.kind),
            )
        temp_trigger = None
        if job.runtime_type == 1:
            temp_dict = {"minutes": job.runtime}

            temp_trigger = self.scheduler._create_trigger(
                trigger="interval", trigger_args=temp_dict)

        if job.runtime_type == 2:
            temp_trigger = CronTrigger.from_crontab(job.runtime)

        if temp_trigger:
            next_run_time = temp_trigger.get_next_fire_time(
                None, datetime.datetime.now(utc))

            self.scheduler.modify_job(
                job.id,
                name=job.name,
                func=callback,
                trigger=temp_trigger,
                next_run_time=next_run_time,
                args=(job, ),
            )

        return job

    # @logger.catch
    def remove_job(
        self,
        id: str,
    ):
        self.scheduler.remove_job(id)

    def pause_job(
        self,
        id: str,
    ):
        self.scheduler.pause_job(id)

    def resume_job(
        self,
        id: str,
    ):
        self.scheduler.pause_job(id)

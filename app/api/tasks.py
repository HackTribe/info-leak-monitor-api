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

from typing import List
from fastapi import APIRouter, Depends, HTTPException, Security, Response
from loguru import logger
from starlette.status import HTTP_403_FORBIDDEN

from app.services.tasks import TaskService
from app.core.security import verify_access_token
from app.schemas.tasks import ResponseTaskInfo, TaskInfo, UpdateTaskInfo

router = APIRouter(
    prefix="/tasks",
    dependencies=[Security(verify_access_token, scopes=["api"])])


@router.get("", response_model=List[ResponseTaskInfo])
async def get_task_all(
        response: Response,
        task_service: TaskService = Depends(TaskService),
):

    tasks = task_service.get_jobs()
    total = len(tasks)
    response.headers.update({
        "X-Total-Count": str(total),
    })
    return tasks


@router.get("/{kind}", response_model=List[ResponseTaskInfo])
async def get_task_by_kind(
        kind: str,
        response: Response,
        task_service: TaskService = Depends(TaskService),
):

    tasks = task_service.get_jobs_by_kind(kind)
    total = len(tasks)
    response.headers.update({
        "X-Total-Count": str(total),
    })
    return tasks


@router.post("", response_model=ResponseTaskInfo)
async def add_task(
        task: TaskInfo,
        task_service: TaskService = Depends(TaskService),
):
    try:
        return task_service.add_job(task, )
    except Exception as e:
        logger.debug("add task: {}", e)
        raise HTTPException(
            status_code=HTTP_403_FORBIDDEN,
            detail="添加失败！",
        )


@router.put("", response_model=ResponseTaskInfo)
async def modify_task(
        task: UpdateTaskInfo,
        task_service: TaskService = Depends(TaskService),
):
    try:
        return task_service.modify_job(task)
    except Exception as e:
        logger.debug(e)
        raise HTTPException(
            status_code=HTTP_403_FORBIDDEN,
            detail="更新失败！",
        )


@router.put("/manager/{id}")
async def pause_task(
        id: str,
        task_service: TaskService = Depends(TaskService),
):
    try:
        return task_service.pause_job(id, )
    except Exception:
        raise HTTPException(
            status_code=HTTP_403_FORBIDDEN,
            detail="'{0}' not existed.".format(id),
        )


@router.patch("/manager/{id}")
async def resume_task(
        id: str,
        task_service: TaskService = Depends(TaskService),
):
    try:
        return task_service.resume_job(id, )
    except Exception:
        raise HTTPException(
            status_code=HTTP_403_FORBIDDEN,
            detail="'{0}' not existed.".format(id),
        )


@router.delete("/{id}")
async def remove_task(
        id: str,
        task_service: TaskService = Depends(TaskService),
):
    try:
        return task_service.remove_job(id, )
    except Exception:
        raise HTTPException(
            status_code=HTTP_403_FORBIDDEN,
            detail="'{0}' not existed.".format(id),
        )

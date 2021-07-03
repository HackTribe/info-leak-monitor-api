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

import re
from concurrent.futures import ThreadPoolExecutor

import dateutil.parser
import gitlab
import requests
from loguru import logger
from app.core.config import settings
from app.repositories.leaks import LeakRepository
from app.repositories.whitelist import WhiteListRepository
from app.schemas.tasks import TaskInfo
from app.schemas.leaks import LeakInfo
from app.tasks.gitbase import (
    get_available_token,
    session_maker,
    MAX_WORKER,
)


def do(job: TaskInfo):
    try_num = 0
    gl = None
    if not job.kind:
        return
    token = get_available_token(job.kind)

    while True:
        try:
            gl = gitlab.Gitlab(settings.gitlab_repository,
                               private_token=token,
                               api_version="4")
            gl.auth()
            break
        except Exception as e:
            logger.error("{} token: <{}>, {}", settings.gitlab_repository,
                         token, e)
            if 3 < try_num:
                return
            try_num += 1

    response = requests.get("{}/api/v4/projects?private_token={}".format(
        settings.gitlab_repository, token))
    total = response.headers.get("X-Total", 0)
    total_pages = response.headers.get("X-Total-Pages", 0)

    logger.debug("current projects <{}>, pages <{}>", total, total_pages)

    _executor = ThreadPoolExecutor(
        max_workers=min(int(total_pages), MAX_WORKER))

    for index in range(1, int(total_pages)):

        def callback(f):
            exc, tb = (f.exception_info() if hasattr(f, "exception_info") else
                       (f.exception(),
                        getattr(f.exception(), "__traceback__", None)))
            if exc:
                logger.error("{0} - work failed, exception: {1}", exc, tb)
            else:
                logger.info("{0} - search code done", job.kind)

        logger.debug("submit {} - keywords {}", index, job.keywords)

        _executor.submit(
            searching,
            job,
            gl,
            index,
        ).add_done_callback(callback)

    _executor.shutdown(wait=True)


def searching(job: TaskInfo, gl: gitlab.Gitlab, page: int):

    # all=True
    repos = gl.projects.list(all=False, simple=False, page=page)
    for repo in repos:
        for keyword in job.keywords:
            # 去掉html标记与换行符
            new_keyword = (re.sub(r"</?\w+[^>]*>", "",
                                  keyword).replace("\r\n",
                                                   "").replace("\n", ""))
            logger.debug("{} searching: {}", job.kind, new_keyword)
            try:
                result = repo.search("blobs", new_keyword)
            except Exception as e:
                logger.error(e)
                continue
            if result:
                get_file(job, new_keyword, repo, result)


def get_file(job: TaskInfo, keyword: str, repo, content_files):
    logger.debug("repo data: {}", repo)
    for _file in content_files:
        try:
            result = repo.files.get(_file["filename"], ref=_file["ref"])
            commit = repo.commits.get(result.last_commit_id)
            if result:
                username = None

                if hasattr(repo, "owner"):
                    username = repo.owner["username"]
                    user_url = "{}/{}".format(settings.gitlab_repository,
                                              username)
                else:
                    username = repo.path_with_namespace
                    user_url = repo.http_url_to_repo
                new_result = {
                    "kind":
                    job.kind,
                    "leakiest":
                    keyword,
                    "html_url":
                    "{}/blob/{}/{}".format(repo.web_url, _file["ref"],
                                           _file["filename"]),
                    "sha":
                    result.content_sha256,
                    "fragment":
                    _file["data"],
                    "user_url":
                    user_url,
                    "user_name":
                    username,
                    "user_avatar":
                    repo.avatar_url,
                    "repo_url":
                    repo.http_url_to_repo,
                    "file_name":
                    _file["filename"],
                    "repo_name":
                    repo.path,
                    "last_modified":
                    dateutil.parser.parse(commit.committed_date),
                }

                logger.debug("result: {}", new_result)

                with session_maker() as db:
                    if WhiteListRepository(db=db).is_existed(
                            new_result["sha"]):
                        continue
                    exclude_flag = False
                    if job.excludes:
                        for exclude in job.excludes:
                            if exclude in new_result["fragment"]:
                                exclude_flag = True
                                break
                    if exclude_flag:
                        continue
                    leak_repo = LeakRepository(db=db)
                    leakage_existed = leak_repo.get_leak_by_sha(
                        new_result["sha"])
                    if leakage_existed:
                        leakage_existed.leak_count += 1
                        leakage_existed.last_modified = dateutil.parser.parse(
                            commit.committed_date)
                        db.commit()
                        # db.flush()
                    else:
                        leak_repo.add(LeakInfo(**new_result))

        except Exception as e:
            logger.error(e)


def name() -> str:
    return "gitlab"

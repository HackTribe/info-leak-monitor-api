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
import time
import re
import math
import threading
import dateutil.parser
from typing import List
from app.repositories.whitelist import WhiteListRepository
from app.repositories.leaks import LeakRepository
from app.schemas.leaks import LeakInfo
from app.tasks.gitbase import (
    get_available_token,
    get_reset_token,
    PER_SUBMIT_NUM,
    session_maker,
    submit,
    MAX_WORKER,
)
from concurrent.futures import ThreadPoolExecutor
from app.schemas.tasks import TaskInfo
from loguru import logger
from urllib3.exceptions import ReadTimeoutError
from github import Github, GithubException
from github.GithubException import UnknownObjectException

PER_PAGE: int = 50


def do(job: TaskInfo):
    logger.info("{0} - searching code.", job.kind)
    if not job.kind:
        return
    if not job.keywords:
        return
    knum = len(job.keywords)
    pages = math.ceil(knum / PER_SUBMIT_NUM)
    if get_available_token(job.kind):
        _executor = ThreadPoolExecutor(max_workers=min(int(pages), MAX_WORKER))

        submit(_executor, searching, job, pages)

        _executor.shutdown(wait=True)
    else:
        logger.error("{0} job not setting access token, it's will not work.",
                     job.name)


def get_new_session():
    token = get_available_token("github")
    if token:
        return Github(login_or_token=token, per_page=PER_PAGE), token
    return None, token


def search_code(keyword: str):
    response = None
    total = None
    try_num = 0
    session, token = get_new_session()
    while True:
        try:
            if session:
                response = session.search_code(keyword,
                                               sort="indexed",
                                               order="desc",
                                               highlight=True)

                total = min(response.totalCount, 1000)
                if total:
                    logger.debug("token {} search {} ok.", token, keyword)
                    break
            else:
                session, token = get_new_session()
                if not token:
                    time.sleep(0.5)
                continue
        except GithubException as e:
            thread_id = threading.currentThread().ident
            logger.debug(
                "GithubException: thread - {}, token - {}, keyword - {}, rate_limit - {}",
                thread_id,
                token,
                keyword,
                e,
            )
            if e.status == 403:
                if token:
                    get_reset_token(session.rate_limiting_resettime, token)
                session, token = get_new_session()
                continue
            else:
                break

        except ReadTimeoutError as e:
            logger.error("Read time out. {0}", e)
            if try_num > 3:
                break
            try_num += 1
            continue

    return response, total


def get_data(github_file, keyword) -> dict:
    def format_fragments(text_matches):
        return "".join([f["fragment"] for f in text_matches])

    if not github_file.last_modified:
        try:
            github_file.update()
        except UnknownObjectException:
            pass
    repo = github_file.repository
    last_modified = (dateutil.parser.parse(github_file.last_modified)
                     if github_file.last_modified else None)

    return {
        "kind": "github",
        "leakiest": keyword,
        "sha": github_file.sha,
        "fragment": format_fragments(github_file.text_matches),
        "html_url": github_file.html_url,
        "last_modified": last_modified,
        "file_name": github_file.name,
        "repo_name": repo.name,
        "repo_url": repo.html_url,
        "user_avatar": repo.owner.avatar_url,
        "user_name": repo.owner.login,
        "user_url": repo.owner.html_url,
    }


def process(job: TaskInfo, contents, keyword: str):
    def check_match(exclude, fragment):
        if exclude in fragment:
            return True
        return False

    for items in contents:
        # repository = items.repository
        # user = repository.owner.login
        # repo_name = repository.name

        with session_maker() as db:
            if WhiteListRepository(db=db).is_existed(items.sha):
                continue

            # check existed leakages
            try:
                leak_repo = LeakRepository(db)
                leakage_existed = leak_repo.get_leak_by_sha(items.sha)
                if leakage_existed:
                    leakage_existed.leak_count += 1
                    db.commit()
                    db.flush()
                else:
                    data = get_data(items, keyword)
                    exclude_flag = False
                    if not job.excludes:
                        job.excludes = []
                    for exclude in job.excludes:
                        if check_match(exclude, data["fragment"]):
                            exclude_flag = True
                            break
                    if exclude_flag:
                        continue
                    if check_match(keyword, data["fragment"]):
                        leak_repo.add(LeakInfo(**data))
            except Exception as e:
                logger.error(e)


def get_next_page(job: TaskInfo, response, max_pages: int, keyword: str):
    page = 0
    try_num = 0
    while page < max_pages:
        try:
            page_contents = response.get_page(page)
            page += 1
            process(job, page_contents, keyword)
        except GithubException as e:
            logger.debug("get page exception: {} - {}", keyword, e)
            break

        except ReadTimeoutError:
            if try_num > 3:
                break
            try_num += 1
            continue


def searching(job: TaskInfo, keywords: List[str]):
    for keyword in keywords:
        # 去掉html标记与换行符
        new_keyword = (re.sub(r"</?\w+[^>]*>", "",
                              keyword).replace("\r\n", "").replace("\n", ""))

        response, total = search_code(new_keyword)
        if response and total:
            max_page = ((total // PER_PAGE) if (not total % PER_PAGE) else
                        (total // PER_PAGE + 1))
            pages = min(max_page, job.pages) if job.pages else max_page
            get_next_page(job, response, pages, new_keyword)


def name() -> str:
    return "github"

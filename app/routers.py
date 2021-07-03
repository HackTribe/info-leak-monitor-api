#
# Copyright (C) 2021
#
# Author: hacktribe <hacktribe.org>
#

from app.api import home, tasks, tokens, leaks, whitelist
from fastapi import APIRouter

router = APIRouter()
router.include_router(home.router, tags=["home"])
router.include_router(home.user, tags=["user"])
router.include_router(tasks.router, tags=["task"])
router.include_router(tokens.router, tags=["tokens"])
router.include_router(leaks.router, tags=["leaks"])
router.include_router(whitelist.router, tags=["whitelist"])

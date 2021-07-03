#
# Copyright (C) 2021
#
# Author: hacktribe <hacktribe.org>
#

from typing import Tuple
from app.core.deps import get_db
from sqlalchemy.orm import Session
from fastapi import Depends


class Repository:
    db: Session
    per: int = 10

    def __init__(self, db: Session = Depends(get_db)):
        self.db = db

    def get_offset(self, per: int, page: int) -> Tuple:
        per = per or self.per
        page -= 1
        if page < 1:
            page = 0
        else:
            page *= per

        return (per, page)

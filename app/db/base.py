#
# Copyright (C) 2021
#
# Author: hacktribe <hacktribe.org>
#

import time

from sqlalchemy import Column, Integer, BigInteger
from sqlalchemy.ext.declarative import as_declarative, declared_attr


@as_declarative()
class Base:
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    create_time = Column(BigInteger, default=time.time)
    update_time = Column(
        BigInteger,
        default=time.time,
        onupdate=time.time,
    )
    is_drop = Column(Integer, default=0)
    __name__: str

    @declared_attr
    def __tablename__(cls) -> str:
        import re

        name_list = re.findall(r"[A-Z][a-z\d]*", cls.__name__)
        return "_".join(name_list).lower()

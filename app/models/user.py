#
# Copyright (C) 2021
#
# Author: hacktribe <hacktribe.org>
#

from app.db.base import Base
from sqlalchemy import Column, String


class User(Base):
    __tablename__ = "users"
    username = Column(String(32), nullable=False, unique=True)
    password = Column(String(255), nullable=False)
    email = Column(String(255), nullable=True, unique=True)

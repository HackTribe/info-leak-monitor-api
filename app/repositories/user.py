#
# Copyright (C) 2021
#
# Author: hacktribe <hacktribe.org>
#
from typing import Optional
from app.core.security import get_password_hash, verify_password
from app.models.user import User
from app.schemas.user import UserRegister

from . import Repository


class UserRepository(Repository):
    def create(self, userinfo: UserRegister) -> User:
        password = get_password_hash(userinfo.password)
        user = User()
        user.username = userinfo.username
        user.password = password
        user.email = userinfo.email
        self.db.add(user)
        self.db.commit()
        return user

    def authenticate(self, username: str, password: str) -> Optional[User]:
        user = self.get_by_username(username)

        if not user:
            return None

        if not verify_password(password, user.password):
            return None

        return user

    def get_by_username(self, username: str) -> User:
        return self.db.query(User).filter(User.username == username).first()

    def get_by_email(self, email: str) -> User:
        return self.db.query(User).filter(User.email == email).first()

    def update_password(self, username: str, new_password: str):
        user = self.get_by_username(username)
        if user:
            user.password = get_password_hash(new_password)
            self.db.commit()

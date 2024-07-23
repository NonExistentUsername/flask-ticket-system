import hashlib
import hmac
from typing import Optional

import jwt
from kytool.domain.base import BaseModel

from flask_ticket_system.domain.rbac.group import Group


def get_password_hash(password: str) -> str:
    return hashlib.sha512(password.encode(), usedforsecurity=True).hexdigest()


def check_password(password: str, password_hash: str) -> bool:
    return hmac.compare_digest(get_password_hash(password), password_hash)


class User(BaseModel):
    def __init__(
        self,
        username: str,
        password: Optional[str] = None,
        password_hash: Optional[str] = None,
        groups: Optional[list[Group]] = None,
        id: Optional[int] = None,
    ):
        super().__init__()
        self.id = id
        self.username = username
        self.groups = groups or []
        self.password_hash = password_hash or get_password_hash(password or "")

    def check_password(self, password: str) -> bool:
        return check_password(password, self.password_hash)

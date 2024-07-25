import hashlib
import hmac
from typing import Optional

import jwt
from kytool.domain.base import BaseModel

from flask_ticket_system import config
from flask_ticket_system.domain import exceptions
from flask_ticket_system.domain.rbac.group import Group
from flask_ticket_system.domain.rbac.permission import Permission


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
        is_superuser: Optional[bool] = False,
    ):
        super().__init__()
        self.id = id
        self.username = username
        self.groups = groups or []
        self.is_superuser = is_superuser
        self.password_hash = password_hash or get_password_hash(password or "")

    def check_password(self, password: str) -> bool:
        return check_password(password, self.password_hash)

    def has_permission(self, permission: Permission) -> bool:
        if self.is_superuser:
            return True
        return any(group.has_permission(permission) for group in self.groups)

    def create_token(self) -> str:
        return str(
            jwt.encode(
                {"id": self.id},
                config.get_secret_key(),
                algorithm="HS256",
            )
        )

    @staticmethod
    def decode_token(token: str) -> dict:
        try:
            return jwt.decode(
                token, config.get_secret_key(), algorithms=["HS256"], verify=True
            )
        except (
            jwt.ExpiredSignatureError,
            jwt.InvalidTokenError,
            jwt.InvalidSignatureError,
        ) as e:
            raise exceptions.UnauthorizedException("Unauthorized") from e

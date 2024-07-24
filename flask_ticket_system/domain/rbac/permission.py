import hashlib
import hmac
from typing import Optional

import jwt
from kytool.domain.base import BaseModel


class Permission(BaseModel):
    def __init__(
        self,
        name: str,
        key: str,
        id: Optional[int] = None,
    ):
        super().__init__()
        self.id = id
        self.name = name
        self.key = key

    @staticmethod
    def from_key(key: str) -> "Permission":
        return Permission(name=key, key=key)

    def __eq__(self, other):
        return isinstance(other, Permission) and self.key == other.key

    def __hash__(self):
        return hash(self.key)

    def __repr__(self):
        return f"<Permission {self.name}: {self.key}>"

    def __str__(self):
        return self.name

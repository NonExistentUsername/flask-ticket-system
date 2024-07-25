import hashlib
import hmac
from typing import Optional

from kytool.domain.base import BaseModel


class Permission(BaseModel):
    def __init__(
        self,
        key: str,
    ):
        super().__init__()
        self.key = key

    @staticmethod
    def from_key(key: str) -> "Permission":
        return Permission(key=key)

    def __eq__(self, other):
        return isinstance(other, Permission) and self.key == other.key

    def __hash__(self):
        return hash(self.key)

    def __repr__(self):
        return f"<Permission: {self.key}>"

    def __str__(self):
        return self.key

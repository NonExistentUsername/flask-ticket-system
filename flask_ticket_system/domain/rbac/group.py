from typing import Optional

from kytool.domain.base import BaseModel

from flask_ticket_system.domain.rbac.permission import Permission


class Group(BaseModel):
    def __init__(
        self,
        name: str,
        permissions: Optional[list[Permission]] = None,
        id: Optional[int] = None,
    ):
        super().__init__()
        self.id = id
        self.name = name
        self.permissions = permissions or []

    def add_permission(self, permission: Permission):
        self.permissions.append(permission)

    def remove_permission(self, permission: Permission):
        self.permissions.remove(permission)

    def has_permission(self, permission: Permission):
        return permission in self.permissions

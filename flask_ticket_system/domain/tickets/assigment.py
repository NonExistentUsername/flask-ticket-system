import enum
from typing import Optional

from kytool.domain.base import BaseModel

from flask_ticket_system.domain.exceptions import AssigmentException
from flask_ticket_system.domain.rbac.permission import Permission


class AssigmentType(enum.Enum):
    USER = "user"
    GROUP = "group"

    @staticmethod
    def from_string(string: str) -> "AssigmentType":
        if string.lower() == "user":
            return AssigmentType.USER
        elif string.lower() == "group":
            return AssigmentType.GROUP
        else:
            raise AssigmentException(f"Invalid AssigmentType: {string}")


class Assigment(BaseModel):
    def __init__(
        self,
        object_type: AssigmentType,
        object_id: int,
    ):
        super().__init__()
        self.object_type = object_type
        self.object_id = object_id

from typing import Optional

from kytool.domain.base import BaseModel

from flask_ticket_system.domain.exceptions import AssigmentException


class AssigmentType:
    USER = "user"
    GROUP = "group"


class Assigment(BaseModel):
    def __init__(
        self,
        object_type: AssigmentType,
        object_id: int,
    ):
        super().__init__()
        self.object_type = object_type
        self.object_id = object_id

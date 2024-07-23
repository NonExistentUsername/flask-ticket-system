from typing import Optional

from kytool.domain.base import BaseModel

from flask_ticket_system.domain.exceptions import AssigmentException


class Assigment(BaseModel):
    def __init__(
        self,
        user_id: Optional[int] = None,
        group_id: Optional[int] = None,
    ):
        super().__init__()
        self.user_id = user_id
        self.group_id = group_id

        if not user_id and not group_id:
            raise AssigmentException("Either user_id or group_id must be provided")

from __future__ import annotations

import enum
from typing import TYPE_CHECKING, Optional

from kytool.domain.base import BaseModel

from flask_ticket_system.domain.tickets.assigment import Assigment

if TYPE_CHECKING:
    from flask_ticket_system.domain.rbac import Group, User


class TicketStatus(enum.IntEnum):
    PENDING = 1
    IN_PROGRESS = 2
    DONE = 3


class Ticket(BaseModel):
    def __init__(
        self,
        title: str,
        description: str,
        status: TicketStatus,
        assigment: Assigment,
        id: Optional[int] = None,
    ):
        super().__init__()
        self.id = id
        self.title = title
        self.description = description
        self.status = status
        self.assigment = assigment

    @staticmethod
    def create(
        title: str,
        description: str,
        status: TicketStatus,
        user: Optional["User"] = None,
        group: Optional["Group"] = None,
    ) -> "Ticket":
        if not user and not group:
            raise ValueError("Either user or group must be provided")

        assigment = Assigment(
            user_id=user.id if user else None, group_id=group.id if group else None
        )

        return Ticket(
            title=title, description=description, status=status, assigment=assigment
        )

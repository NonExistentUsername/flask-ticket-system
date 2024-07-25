from __future__ import annotations

import enum
from typing import TYPE_CHECKING, Optional

from kytool.domain.base import BaseModel

from flask_ticket_system.domain.events import TicketCreated
from flask_ticket_system.domain.tickets.assigment import Assigment

if TYPE_CHECKING:
    from flask_ticket_system.domain.rbac import Group, Permission, User


class TicketStatus(enum.IntEnum):
    PENDING = 1
    IN_PROGRESS = 2
    DONE = 3

    @staticmethod
    def from_string(status: str) -> TicketStatus:
        return TicketStatus[status.upper()]


class Ticket(BaseModel):
    def __init__(
        self,
        title: str,
        content: str,
        status: TicketStatus,
        assigment: Assigment,
        id: Optional[int] = None,
    ):
        super().__init__()
        self.id = id
        self.title = title
        self.content = content
        self.status = status
        self.assigment = assigment

    @staticmethod
    def create(
        title: str,
        content: str,
        assigment: Assigment,
    ) -> "Ticket":
        ticket = Ticket(
            title=title,
            content=content,
            status=TicketStatus.PENDING,
            assigment=assigment,
        )
        ticket.events.append(TicketCreated(ticket))
        return ticket

    def can_view(self, user: User) -> bool:
        if user.is_superuser:
            return True

        if self.assigment.object_type == "group":
            return user.has_permission(
                Permission(
                    name="Ticket view",
                    key=f"ticket:group:{self.assigment.object_id}",
                )
            )

        return user.id == self.assigment.object_id

    def can_change_status(self, user: User) -> bool:
        if user.is_superuser:
            return True

        if self.assigment.object_type == "group":
            return user.has_permission(
                Permission(
                    name="Ticket change status",
                    key=f"ticket:group:{self.assigment.object_id}",
                )
            )

        return user.id == self.assigment.object_id

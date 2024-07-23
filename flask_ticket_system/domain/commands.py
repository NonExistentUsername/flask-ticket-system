from kytool.domain.commands import Command

from flask_ticket_system.domain.tickets.ticket import TicketStatus


class CreateTicketCommand(Command):
    def __init__(
        self,
        title: str,
        content: str,
        assigned_user_id: int,
        assigned_group_id: int,
        status: TicketStatus = TicketStatus.PENDING,
    ):
        self.title = title
        self.content = content
        self.assigned_user_id = assigned_user_id
        self.assigned_group_id = assigned_group_id
        self.status = status

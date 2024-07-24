from kytool.domain.commands import Command

from flask_ticket_system.domain.tickets.assigment import Assigment
from flask_ticket_system.domain.tickets.ticket import TicketStatus


class CreateTicketCommand(Command):
    def __init__(
        self,
        title: str,
        content: str,
        assigment: Assigment,
        status: TicketStatus = TicketStatus.PENDING,
    ):
        self.title = title
        self.content = content
        self.assignment = assigment
        self.status = status

from typing import TYPE_CHECKING

from kytool.domain.events import Event

if TYPE_CHECKING:
    from flask_ticket_system.domain.tickets.ticket import Ticket


class TicketCreated(Event):
    def __init__(self, ticket: "Ticket"):
        super().__init__()
        self.ticket = ticket

from kytool.domain.events import Event

from flask_ticket_system.domain.tickets.ticket import Ticket


class TicketCreated(Event):
    def __init__(self, ticket: Ticket):
        super().__init__()
        self.ticket = ticket

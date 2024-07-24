from kytool.adapters.repository import AbstractRepository
from kytool.service_layer.handlers import register_handler

from flask_ticket_system.domain import Ticket, TicketStatus, User
from flask_ticket_system.domain.commands import CreateTicketCommand
from flask_ticket_system.service_layer.unit_of_work import AbstractUnitOfWork


@register_handler(CreateTicketCommand)
def create_ticket_handler(
    command: CreateTicketCommand,
    uow: AbstractUnitOfWork,
) -> Ticket:
    ticket = Ticket.create(
        title=command.title,
        content=command.content,
        assigment=command.assignment,
    )
    uow.tickets.add(ticket)
    uow.commit()
    return ticket

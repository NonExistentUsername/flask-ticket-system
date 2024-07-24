from kytool.adapters.repository import AbstractRepository
from kytool.service_layer.handlers import register_handler

from flask_ticket_system.domain import (
    InvalidCredentialsException,
    Ticket,
    TicketStatus,
    User,
)
from flask_ticket_system.domain.commands import CreateTicketCommand, LoginCommand
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


@register_handler(LoginCommand)
def login_handler(
    command: LoginCommand,
    uow: AbstractUnitOfWork,
) -> str:
    user = uow.users.get(username=command.username)

    if not user:
        raise InvalidCredentialsException("Invalid username")

    if not user.check_password(command.password):
        raise InvalidCredentialsException("Invalid password")

    return user.create_token()

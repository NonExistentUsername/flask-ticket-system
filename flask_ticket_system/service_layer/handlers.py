from kytool.adapters.repository import AbstractRepository
from kytool.service_layer.handlers import register_handler

from flask_ticket_system.domain import (
    InvalidCredentialsException,
    Ticket,
    TicketStatus,
    User,
    commands,
    exceptions,
)
from flask_ticket_system.service_layer.unit_of_work import AbstractUnitOfWork


@register_handler(commands.CreateTicketCommand)
def create_ticket_handler(
    command: commands.CreateTicketCommand,
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


@register_handler(commands.LoginCommand)
def login_handler(
    command: commands.LoginCommand,
    uow: AbstractUnitOfWork,
) -> str:
    user = uow.users.get(username=command.username)

    if not user:
        raise InvalidCredentialsException("Invalid username")

    if not user.check_password(command.password):
        raise InvalidCredentialsException("Invalid password")

    return user.create_token()


@register_handler(commands.GetTicketCommand)
def get_ticket(
    command: commands.GetTicketCommand,
    uow: AbstractUnitOfWork,
) -> Ticket:
    decoded_token = User.decode_token(command.token)
    user = uow.users.get(id=decoded_token.get("id", -1))

    if not user:
        raise exceptions.UnauthorizedException("User not found")

    ticket = uow.tickets.get(id=command.ticket_id)

    if not ticket:
        raise exceptions.TicketNotFoundException("Ticket not found")

    if not ticket.can_access(user):
        raise exceptions.UnauthorizedException("Unauthorized")

    return ticket

from kytool.adapters.repository import AbstractRepository
from kytool.service_layer.handlers import register_handler

from flask_ticket_system.domain import (
    Group,
    InvalidCredentialsException,
    Permission,
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

    if not ticket.can_view(user):
        raise exceptions.UnauthorizedException("Unauthorized")

    return ticket


@register_handler(commands.CreateGroupCommand)
def create_group(
    command: commands.CreateGroupCommand,
    uow: AbstractUnitOfWork,
):
    decoded_token = User.decode_token(command.token)
    user = uow.users.get(id=decoded_token.get("id", -1))

    if not user:
        raise exceptions.UnauthorizedException("User not found")

    if not user.is_superuser:
        raise exceptions.UnauthorizedException("Unauthorized")

    group = Group(name=command.name)
    uow.groups.add(group)
    uow.commit()
    return group


@register_handler(commands.AddUserToGroupCommand)
def add_user_to_group(
    command: commands.AddUserToGroupCommand,
    uow: AbstractUnitOfWork,
):
    decoded_token = User.decode_token(command.token)
    user = uow.users.get(id=decoded_token.get("id", -1))

    if not user:
        raise exceptions.UnauthorizedException("User not found")

    if not user.is_superuser:
        raise exceptions.UnauthorizedException("Unauthorized")

    group = uow.groups.get(id=command.group_id)
    if not group:
        raise exceptions.GroupNotFoundException("Group not found")

    user = uow.users.get(id=command.user_id)
    if not user:
        raise exceptions.UserNotFoundException("User not found")

    user.groups.append(group)
    uow.commit()
    return group


@register_handler(commands.AddPermissionToGroupCommand)
def add_permission_to_group(
    command: commands.AddPermissionToGroupCommand,
    uow: AbstractUnitOfWork,
):
    decoded_token = User.decode_token(command.token)
    user = uow.users.get(id=decoded_token.get("id", -1))

    if not user:
        raise exceptions.UnauthorizedException("User not found")

    if not user.is_superuser:
        raise exceptions.UnauthorizedException("Unauthorized")

    group = uow.groups.get(id=command.group_id)
    if not group:
        raise exceptions.GroupNotFoundException("Group not found")

    group.permissions.append(Permission(key=command.permission))
    uow.commit()
    return group


@register_handler(commands.UpdateTicketCommand)
def update_ticket(
    command: commands.UpdateTicketCommand,
    uow: AbstractUnitOfWork,
):
    decoded_token = User.decode_token(command.token)
    user = uow.users.get(id=decoded_token.get("id", -1))

    if not user:
        raise exceptions.UnauthorizedException("User not found")

    ticket = uow.tickets.get(id=command.ticket_id)

    if not ticket:
        raise exceptions.TicketNotFoundException("Ticket not found")

    if not ticket.can_change_status(user):
        raise exceptions.UnauthorizedException("Unauthorized")

    ticket.status = command.status
    uow.commit()
    return ticket


@register_handler(commands.CreateUserCommand)
def create_user(
    command: commands.CreateUserCommand,
    uow: AbstractUnitOfWork,
):
    user = User(
        username=command.username,
        password=command.password,
        is_superuser=command.is_superuser,
    )
    uow.users.add(user)
    uow.commit()
    return user

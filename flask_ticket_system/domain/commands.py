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


class LoginCommand(Command):
    def __init__(
        self,
        username: str,
        password: str,
    ):
        self.username = username
        self.password = password


class GetTicketCommand(Command):
    def __init__(
        self,
        ticket_id: int,
        token: str,
    ):
        self.ticket_id = ticket_id
        self.token = token


class UpdateTicketCommand(Command):
    def __init__(
        self,
        ticket_id: int,
        status: TicketStatus,
        token: str,
    ):
        self.ticket_id = ticket_id
        self.status = status
        self.token = token


class CreateGroupCommand(Command):
    def __init__(
        self,
        name: str,
        token: str,
    ):
        self.name = name
        self.token = token


class AddUserToGroupCommand(Command):
    def __init__(
        self,
        user_id: int,
        group_id: int,
        token: str,
    ):
        self.user_id = user_id
        self.group_id = group_id
        self.token = token


class AddPermissionToGroupCommand(Command):
    def __init__(
        self,
        permission: str,
        group_id: int,
        token: str,
    ):
        self.permission = permission
        self.group_id = group_id
        self.token = token

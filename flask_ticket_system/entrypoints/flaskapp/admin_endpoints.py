from flask import Response, jsonify, request
from pydantic import ValidationError

from flask_ticket_system.domain import Group, User, commands, exceptions
from flask_ticket_system.domain.tickets import Assigment, AssigmentType, Ticket
from flask_ticket_system.entrypoints.flaskapp.messagebus import message_bus
from flask_ticket_system.entrypoints.flaskapp.middleware import (
    authorization_middleware,
    model_middleware,
)
from flask_ticket_system.entrypoints.flaskapp.schemes import (
    AddPermissionToGroup,
    AddUserToGroup,
)
from flask_ticket_system.entrypoints.flaskapp.schemes import Assigment as PAssigment
from flask_ticket_system.entrypoints.flaskapp.schemes import CreateGroup, CreateUser


@authorization_middleware
@model_middleware(CreateUser)
def create_user(token: str, create_user: CreateUser):
    try:
        user: User = message_bus.handle(
            commands.CreateUserCommand(
                create_user.username,
                create_user.password,
                create_user.is_superuser,
            )
        )
    except exceptions.UserAlreadyExistsException:
        return Response("User already exists", status=400)

    return jsonify(
        {
            "id": user.id,
        }
    )


@model_middleware(CreateGroup)
@authorization_middleware
def create_group(token: str, create_group: CreateGroup):
    try:
        group: Group = message_bus.handle(
            commands.CreateGroupCommand(
                create_group.name,
                token,
            )
        )
    except exceptions.UnauthorizedException:
        return Response(status=401)

    return jsonify(
        {
            "id": group.id,
        }
    )


@model_middleware(AddUserToGroup)
def add_user_to_group(add_user_to_group: AddUserToGroup):
    try:
        message_bus.handle(
            commands.AddUserToGroupCommand(
                add_user_to_group.user_id,
                add_user_to_group.group_id,
                add_user_to_group.token,
            )
        )
    except exceptions.UnauthorizedException:
        return Response(status=401)

    return Response(status=200)


@model_middleware(AddPermissionToGroup)
def add_permission_to_group(add_permission_to_group: AddPermissionToGroup):
    try:
        message_bus.handle(
            commands.AddPermissionToGroupCommand(
                add_permission_to_group.permission,
                add_permission_to_group.group_id,
                add_permission_to_group.token,
            )
        )
    except exceptions.UnauthorizedException:
        return Response(status=401)

    return Response(status=200)

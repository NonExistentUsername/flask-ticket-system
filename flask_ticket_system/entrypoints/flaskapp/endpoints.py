from flask import Response, jsonify, request
from pydantic import ValidationError

from flask_ticket_system.domain import TicketStatus, commands, exceptions
from flask_ticket_system.domain.tickets import Assigment, AssigmentType, Ticket
from flask_ticket_system.entrypoints.flaskapp.messagebus import message_bus
from flask_ticket_system.entrypoints.flaskapp.middleware import (
    authorization_middleware,
    model_middleware,
)
from flask_ticket_system.entrypoints.flaskapp.schemes import Assigment as PAssigment
from flask_ticket_system.entrypoints.flaskapp.schemes import (
    CreateTicket,
    Login,
    UpdateTicket,
)


@model_middleware(CreateTicket)
def create_ticket(create_ticket: CreateTicket):
    ticket: Ticket = message_bus.handle(
        commands.CreateTicketCommand(
            create_ticket.title,
            create_ticket.content,
            Assigment(
                AssigmentType.from_string(create_ticket.assigment.assigment_type),
                create_ticket.assigment.assigment_id,
            ),
        )
    )

    return jsonify(
        {
            "id": ticket.id,
        }
    )


@model_middleware(Login)
def login(login: Login):
    try:
        token: str = message_bus.handle(
            commands.LoginCommand(
                login.username,
                login.password,
            )
        )
    except exceptions.InvalidCredentialsException as e:
        return Response("Invalid credentials", status=401)

    return jsonify(
        {
            "token": token,
        }
    )


@authorization_middleware
def view_ticket(token: str, ticket_id: int):
    try:
        ticket: Ticket = message_bus.handle(commands.GetTicketCommand(ticket_id, token))
    except exceptions.TicketNotFoundException:
        return Response("Ticket not found", status=404)
    except exceptions.UnauthorizedException:
        return Response("Ticket not found", status=404)  # Haha, you will never know

    return jsonify(
        {
            "id": ticket.id,
            "title": ticket.title,
            "content": ticket.content,
            "status": ticket.status,
            "assigment": {
                "assigment_type": ticket.assigment.object_type,
                "assigment_id": ticket.assigment.object_id,
            },
        }
    )


@authorization_middleware
@model_middleware(UpdateTicket)
def update_ticket(token: str, update_ticket: UpdateTicket):
    try:
        ticket: Ticket = message_bus.handle(
            commands.UpdateTicketCommand(
                update_ticket.ticket_id,
                TicketStatus.from_string(update_ticket.status),
                token,
            )
        )
    except exceptions.TicketNotFoundException:
        return Response("Ticket not found", status=404)
    except exceptions.UnauthorizedException:
        return Response("Unauthorized", status=401)

    return jsonify(
        {
            "id": ticket.id,
            "status": ticket.status,
        }
    )

from flask import Response, jsonify, request
from pydantic import ValidationError

from flask_ticket_system.domain.commands import CreateTicketCommand
from flask_ticket_system.domain.tickets import Assigment, Ticket
from flask_ticket_system.entrypoints.flaskapp.messagebus import message_bus
from flask_ticket_system.entrypoints.flaskapp.middleware import model_middleware
from flask_ticket_system.entrypoints.flaskapp.schemes import Assigment as PAssigment
from flask_ticket_system.entrypoints.flaskapp.schemes import CreateTicket


@model_middleware(CreateTicket)
def create_ticket(create_ticket: CreateTicket):
    ticket: Ticket = message_bus.handle(
        CreateTicketCommand(
            create_ticket.title,
            create_ticket.content,
            Assigment(
                create_ticket.assigment.assigment_type,
                create_ticket.assigment.assigment_id,
            ),
        )
    )

    return jsonify(
        {
            "id": ticket.id,
        }
    )

from flask import Response, jsonify, request
from pydantic import ValidationError

from flask_ticket_system.entrypoints.flaskapp.middleware import model_middleware
from flask_ticket_system.entrypoints.flaskapp.schemes import CreateTicket


@model_middleware(CreateTicket)
def create_ticket(create_ticket: CreateTicket):
    return Response(str(create_ticket.model_dump()), status=200)

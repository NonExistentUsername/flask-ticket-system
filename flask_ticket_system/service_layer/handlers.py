from kytool.service_layer.handlers import register_handler

from flask_ticket_system.domain.commands import CreateTicketCommand


@register_handler(CreateTicketCommand)
def create_ticket_handler(command: CreateTicketCommand):
    print("Create ticket handler")

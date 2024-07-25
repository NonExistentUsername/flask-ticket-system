from typing import TYPE_CHECKING

from kytool.factories import create_message_bus

from flask_ticket_system.domain import commands
from flask_ticket_system.service_layer.handlers import *
from flask_ticket_system.service_layer.unit_of_work import InMemoryUnitOfWorkPool

if TYPE_CHECKING:
    from kytool.service_layer.messagebus import MessageBus


def my_create_message_bus() -> "MessageBus":
    msbus = create_message_bus(uow_pool=InMemoryUnitOfWorkPool())

    # Add admin account
    msbus.handle(
        commands.CreateUserCommand(
            username="admin",
            password="admin",
            is_superuser=True,
        )
    )

    return msbus


message_bus: "MessageBus" = my_create_message_bus()

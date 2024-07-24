from typing import TYPE_CHECKING

from kytool.factories import create_message_bus

from flask_ticket_system.service_layer.handlers import *
from flask_ticket_system.service_layer.unit_of_work import InMemoryUnitOfWorkPool

if TYPE_CHECKING:
    from kytool.service_layer.messagebus import MessageBus

message_bus: "MessageBus" = create_message_bus(uow_pool=InMemoryUnitOfWorkPool())

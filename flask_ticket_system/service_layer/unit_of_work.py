from copy import deepcopy
from typing import Any

from kytool.service_layer import unit_of_work

from flask_ticket_system.adapters.repository import (
    AbstractGroupRepository,
    AbstractTicketRepository,
    AbstractUserRepository,
    InMemoryGroupRepository,
    InMemoryTicketRepository,
    InMemoryUserRepository,
)


class AbstractUnitOfWork(unit_of_work.AbstractUnitOfWork):
    def __init__(
        self,
        tickets: AbstractTicketRepository,
        users: AbstractUserRepository,
        groups: AbstractGroupRepository,
    ):
        self.tickets = tickets
        self.users = users
        self.groups = groups


class InMemoryUnitOfWork(AbstractUnitOfWork):
    def __init__(self):
        super().__init__(
            InMemoryTicketRepository(),
            InMemoryUserRepository(),
            InMemoryGroupRepository(),
        )
        self._last_committed = {
            "tickets": deepcopy(self.tickets),
            "users": deepcopy(self.users),
        }

    def commit(self):
        self._last_committed = {
            "tickets": deepcopy(self.tickets),
            "users": deepcopy(self.users),
        }

    def rollback(self):
        self.tickets = self._last_committed["tickets"]
        self.users = self._last_committed["users"]

    def collect_new_events(self):
        for repository in (self.tickets, self.users, self.groups):
            for instance in repository.seen:
                if hasattr(instance, "events") and isinstance(instance.events, list):
                    while instance.events:
                        yield instance.events.pop(0)


class InMemoryUnitOfWorkPool(unit_of_work.AbstractUnitOfWorkPool[AbstractUnitOfWork]):
    def __init__(self):
        super().__init__()
        self.uow = InMemoryUnitOfWork()

    def get(self) -> AbstractUnitOfWork:
        return self.uow

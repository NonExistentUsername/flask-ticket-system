import abc
from typing import Dict, List, Optional
from uuid import uuid4

from kytool.adapters import repository

from flask_ticket_system.domain import (
    Assigment,
    AssigmentType,
    Group,
    Ticket,
    TicketStatus,
    User,
)


class AbstractUserRepository(repository.AbstractRepository[User]):
    pass


class AbstractTicketRepository(repository.AbstractRepository[Ticket]):
    pass


class AbstractGroupRepository(repository.AbstractRepository[Group]):
    pass


class InMemoryUserRepository(
    repository.InMemoryRepository[User], AbstractUserRepository
):
    def __init__(self) -> None:
        super().__init__(query_fields=["id", "username"])

    def _add(self, instance: User) -> None:
        instance.id = uuid4().int
        return super()._add(instance)


class InMemoryTicketRepository(
    repository.InMemoryRepository[Ticket], AbstractTicketRepository
):
    def __init__(self) -> None:
        super().__init__(query_fields=["id", "title"])

    def _add(self, instance: Ticket) -> None:
        instance.id = uuid4().int
        return super()._add(instance)


class InMemoryGroupRepository(repository.InMemoryRepository, AbstractGroupRepository):
    def __init__(self) -> None:
        super().__init__(query_fields=["id", "name"])

    def _add(self, instance: Group) -> None:
        instance.id = int(uuid4().int)
        return super()._add(instance)

from typing import Literal

from pydantic import BaseModel, Field


class Assigment(BaseModel):
    assigment_type: Literal["user", "group"]
    assigment_id: int = Field(..., ge=1)


class CreateTicket(BaseModel):
    title: str = Field(..., min_length=1, max_length=100)
    content: str = Field(..., min_length=1, max_length=1000)
    assigment: Assigment


class Login(BaseModel):
    username: str = Field(..., min_length=1, max_length=100)
    password: str = Field(..., min_length=1, max_length=100)


class UpdateTicket(BaseModel):
    status: Literal["PENDING", "IN_PROGRESS", "DONE"]


class CreateGroup(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)


class AddUserToGroup(BaseModel):
    user_id: int = Field(..., ge=1)
    group_id: int = Field(..., ge=1)


class CreatePermission(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    key: str = Field(..., min_length=1, max_length=100)


class AddPermissionToGroup(BaseModel):
    permission: str = Field(..., min_length=1, max_length=100)
    group_id: int = Field(..., ge=1)


class CreateUser(BaseModel):
    username: str = Field(..., min_length=1, max_length=100)
    password: str = Field(..., min_length=1, max_length=100)
    is_superuser: bool = False

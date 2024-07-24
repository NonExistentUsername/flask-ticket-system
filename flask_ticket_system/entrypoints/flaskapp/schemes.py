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

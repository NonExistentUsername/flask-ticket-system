from pydantic import BaseModel, Field


class Assigment(BaseModel):
    assigment_type: str = Field(..., min_length=1, max_length=100)
    assigment_id: int = Field(..., ge=1)


class CreateTicket(BaseModel):
    title: str = Field(..., min_length=1, max_length=100)
    content: str = Field(..., min_length=1, max_length=1000)
    assigment: Assigment

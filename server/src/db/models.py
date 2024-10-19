from sqlmodel import (
    Field,
    SQLModel,
    Column,
    JSON,
)
from pydantic import BaseModel
from .id import generate_id

class TestModel(SQLModel, table=True):
    id: int = Field(default_factory=generate_id, primary_key=True)
    name: str
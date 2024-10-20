from sqlmodel import (
    Field,
    SQLModel,
    Column,
    JSON,
)
from pydantic import BaseModel
from datetime import datetime, timezone
import uuid
from typing import Optional
from .id import generate_id

class Session(SQLModel, table=True):
    token: str = Field(primary_key=True)
    user_id: Optional[int] = Field(foreign_key="user.id")
    expires_at: datetime = Field(default_factory=datetime.utcnow)
    
class UserPassword(SQLModel, table=True):
    id: Optional[int] = Field(primary_key=True, foreign_key="user.id")
    passhash: str
    
# Use a join to get the data from the collection
class Card(SQLModel, table=True):
    id: int = Field(default_factory=generate_id, primary_key=True)
    content: str = Field()
    created_at: datetime = Field(default_factory=datetime.now)
    image_id: uuid.UUID = Field(default_factory=uuid.uuid4)
    collection_id: Optional[int] = Field(default=None, foreign_key="collection.id")
    
class Collection(SQLModel, table=True):
    id: int = Field(primary_key=True)
    name: str
    description: str
    created_at: datetime = Field(default_factory=datetime.now)
    user_id: Optional[int] = Field(foreign_key="user.id")
    
class User(SQLModel, table=True):
    id: int = Field(default_factory=generate_id, primary_key=True)
    email: str = Field(unique=True)
    name: str
    # collection_id: Optional[Collection] = Field(default=None, foreign_key="collection.id")

    # group_id is the group that the user belongs to.
    # group_id: Optional[int] = Field(default=None, foreign_key="group.id")

    # group_relationships is the relationships that the user has with other
    # groups.
    # group_relationships: list["Group"] = Relationship(link_model=GroupRelationship)

    # @field_validator("genders")
    # @classmethod
    # def validate_genders(cls, genders: list[str]):
    #     for gender in genders:
    #         assert gender in consts.GENDERS

    # @field_validator("pronouns")
    # @classmethod
    # def validate_pronouns(cls, pronouns: list[str]):
    #     for pronoun in pronouns:
    #         assert pronoun in consts.PRONOUNS

    # @field_validator("sexual_orientations")
    # @classmethod
    # def validate_sexual_orientations(cls, sexual_orientations: list[str]):
    #     for sexual_orientation in sexual_orientations:
    #         assert sexual_orientation in consts.SEXUAL_ORIENTATIONS

    # @field_validator("color")
    # @classmethod
    # def validate_color(cls, color: str):
    #     colors.assert_valid_color(color)
    
    
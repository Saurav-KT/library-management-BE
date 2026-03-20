from sqlmodel import Field, Relationship
from app.models.base import BaseModel
from typing import List

class Publisher(BaseModel, table=True):
    publisher_id: int = Field(default=None, primary_key=True)
    publisher_name: str
    address: str | None = None
    phone: int | None = None

    books: List["Book"] = Relationship(back_populates="publisher")
from sqlmodel import Field, Relationship
from app.models.base import BaseModel
from typing import List
class Author(BaseModel, table=True):
    __tablename__ = "author"
    author_id: int = Field(default=None, primary_key=True)
    author_name: str
    country: str | None = None
    birth_year: str| None = None

    books: List["Book"] = Relationship(back_populates="author")
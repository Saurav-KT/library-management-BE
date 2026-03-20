from sqlmodel import Field, Relationship
from app.models.base import BaseModel
from typing import List

class Category(BaseModel, table=True):
    __tablename__ = "category"
    category_id: int = Field(default=None, primary_key=True)
    category_name: str
    description: str | None = None

    books: List["Book"] = Relationship(back_populates="category")
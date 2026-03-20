
from sqlmodel import Field,Relationship
from app.models.base import BaseModel
from typing import List

class Book(BaseModel, table=True):
    __tablename__ = "book"

    book_id: int = Field(default=None, primary_key=True)
    title: str
    isbn: str | None = None
    publication_year: int | None = None
    edition: str | None = None
    pages: int | None = None
    total_copies: int
    available_copies: int

    # Foreign keys
    author_id: int | None = Field(default=None, foreign_key="author.author_id")
    publisher_id: int | None = Field(default=None, foreign_key="publisher.publisher_id")
    category_id: int | None = Field(default=None, foreign_key="category.category_id")

    # Relationships
    author: "Author"  = Relationship(back_populates="books")
    publisher: "Publisher"  = Relationship(back_populates="books")
    category: "Category" = Relationship(back_populates="books")

    # Core library workflow relationships
    copies: List["BookCopy"] = Relationship(back_populates="book")
    borrows: List["Borrow"] = Relationship(back_populates="book")


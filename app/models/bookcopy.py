from sqlmodel import SQLModel, Field, Relationship
from typing import Optional
from app.utils.base_enum import Status
from typing import List

class BookCopy(SQLModel, table=True):
    copy_id: int = Field(default=None, primary_key=True)
    book_id: int = Field(foreign_key="book.book_id")
    status: Status = Field(default=Status.AVAILABLE)
    location: str | None = None

    book: Optional["Book"] = Relationship(back_populates="copies")
    borrows: List["Borrow"] = Relationship(back_populates="book_copy")
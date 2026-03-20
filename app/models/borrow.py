from datetime import date
from typing import Optional
from app.models.base import BaseModel
from sqlmodel import Field, Relationship

class Borrow(BaseModel, table=True):
    borrow_id: int = Field(default=None, primary_key=True)
    member_id: int = Field(foreign_key="member.member_id")
    book_id: int = Field(foreign_key="book.book_id")
    book_copy_id: int = Field(foreign_key="bookcopy.copy_id")
    issue_date: date
    due_date: date
    return_date: date | None = None
    fine: float | None = 0.0

    member: Optional["Member"] = Relationship(back_populates="borrows")
    book: Optional["Book"] = Relationship(back_populates="borrows")
    book_copy: Optional["BookCopy"] = Relationship(back_populates="borrows")
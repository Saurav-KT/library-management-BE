from pydantic import BaseModel
from typing import Optional

class BookBase(BaseModel):
    title: str
    isbn: Optional[str] = None
    publication_year: Optional[int] = None
    edition: Optional[str] = None
    pages: Optional[int] = None
    total_copies: int
    available_copies: int
    author_id: Optional[int] = None
    publisher_id: Optional[int] = None
    category_id: Optional[int] = None

class BookRead(BookBase):
    book_id: int

class BookCreate(BookBase):
    pass

class BookUpdate(BaseModel):
    title: Optional[str] = None
    isbn: Optional[str] = None
    publication_year: Optional[int] = None
    edition: Optional[str] = None
    pages: Optional[int] = None
    total_copies: Optional[int] = None
    available_copies: Optional[int] = None
    author_id: Optional[int] = None
    publisher_id: Optional[int] = None
    category_id: Optional[int] = None


class BookDelete(BaseModel):
    book_id: int

class BookReadWithRelations(BookRead):
    author_name: Optional[str] = None
    publisher_name: Optional[str] = None
    category_name: Optional[str] = None
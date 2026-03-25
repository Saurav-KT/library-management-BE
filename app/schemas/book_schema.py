from pydantic import BaseModel, Field, ConfigDict
from app.schemas.author_schema import AuthorRead
from app.schemas.publisher_schema import PublisherRead
from app.schemas.category_schema import CategoryRead

class BookBase(BaseModel):
    title: str
    isbn: str | None = None
    publication_year: int | None = None
    edition: str | None = None
    pages: int | None = None
    total_copies: int = Field(ge=1)
    available_copies: int = Field(ge=0)
    author_id: int | None = None
    publisher_id: int | None = None
    category_id: int | None = None


class BookRead(BookBase):
    book_id: int
    model_config = ConfigDict(from_attributes=True)


class BookCreate(BookBase):
    pass


class BookUpdate(BaseModel):
    title: str | None = None
    isbn: str | None = None
    publication_year: int | None = None
    edition: str | None = None
    pages: int | None = None
    total_copies: int = Field(le=1)
    available_copies: int = Field(le=1)
    author_id: int | None = None
    publisher_id: int | None = None
    category_id: int | None = None


class BookDelete(BaseModel):
    book_id: int


class BookReadWithRelations(BookRead):
    author: AuthorRead | None
    publisher: PublisherRead | None
    category: CategoryRead | None

from sqlmodel import select

from app.core.exception import ResourceNotFoundException
from app.models.book import Book
from app.schemas.book_schema import BookCreate, BookRead
from app.service.base_service import BaseService


class BookService(BaseService):

    async def create_book(self, book_data: BookCreate) -> BookRead:
            # Create an ORM object
            new_book = Book(**book_data.model_dump())

            # Save to DB
            self.session.add(new_book)
            await self.commit_and_refresh(new_book)

            # Convert ORM to Response Schema
            return BookRead.model_validate(new_book)


    async def get_book_by_id(self, book_id: int) -> BookRead:
            result = await self.session.execute(select(Book).where(Book.book_id == book_id))
            book = result.scalars().first()
            if not book:
                raise ResourceNotFoundException(f"Book with ID {book_id} does not exist")
            return BookRead.model_validate(book)






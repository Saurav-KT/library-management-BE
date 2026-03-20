from sqlmodel import select
from app.core.exception import BaseAppException,ResourceNotFoundException
from datetime import datetime, timezone
from app.schemas.book_schema import BookCreate, BookRead, BookUpdate
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.book import Book

class BookService:

    @staticmethod
    async def create_book(book_data: BookCreate, session: AsyncSession) -> BookRead:
        try:
            # Create an ORM object
            new_book = Book(**book_data.model_dump())

            # Save to DB
            session.add(new_book)
            await session.commit()
            await session.refresh(new_book)

            # Convert ORM to Response Schema
            return BookRead.model_validate(new_book)
        except Exception as e:
            raise BaseAppException("Internal database error") from e

    @staticmethod
    async def get_book_by_id(book_id: int, session: AsyncSession) -> BookRead:
        try:
            result = await session.execute(select(Book).where(Book.book_id == book_id))
            book = result.scalars().first()
            if not book:
                raise ResourceNotFoundException(f"Book with ID {book_id} does not exist")
            return BookRead.model_validate(book)
        except Exception as e:
            raise BaseAppException("Internal database error") from e


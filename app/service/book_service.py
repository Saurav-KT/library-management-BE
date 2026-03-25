from sqlalchemy.orm import selectinload
from sqlmodel import select

from app.core.exception import ResourceNotFoundException, ValidationException
from app.models.book import Book
from app.models.bookcopy import BookCopy

from app.schemas.book_schema import BookCreate, BookRead, BookReadWithRelations, BookUpdate
from app.service.base_service import BaseService
from app.utils.base_enum import Status, Location

class BookService(BaseService):

    async def create_book(self, book_data: BookCreate) -> BookRead:
            # Create an ORM object
            new_book = Book(**book_data.model_dump())

            # Save to DB
            self.session.add(new_book)
            await self.session.flush()
            # 🔥 Create copies
            copies = [
                BookCopy(book_id=new_book.book_id,status=Status.AVAILABLE, location=Location.SHELF)
                for _ in range(new_book.total_copies)
            ]

            self.session.add_all(copies)
            await self.commit_and_refresh(new_book)

            # Convert ORM to Response Schema
            return BookRead.model_validate(new_book)

    async def get_books(self)->list[BookReadWithRelations]:
            result = await self.session.execute(
                select(Book)
                .options(
                    selectinload(Book.author),
                    selectinload(Book.publisher),
                    selectinload(Book.category),
                )
            )

            books = result.scalars().all()
            return [BookReadWithRelations.model_validate(book) for book in books]

    async def update_book(self, book_id: int, book_obj: BookUpdate)-> BookRead:

            update_data=book_obj.model_dump(exclude_unset=True)
            if not update_data:
                raise ValidationException("No fields provided for update")

            result = await self.session.execute(select(Book).where(Book.book_id == book_id))
            book = result.scalar_one_or_none()
            if not book:
                raise ResourceNotFoundException(f"Book with ID {book_id} does not exist")

            # if new_total < issued_books:
            #     raise ValidationException("Cannot reduce below issued books")
            book.sqlmodel_update(update_data)
            # update to DB
            self.session.add(book)
            await self.commit_and_refresh(book)
            # Return updated DB object
            return BookRead.model_validate(book)



    async def get_book_by_id(self, book_id: int) -> BookRead:
            result = await self.session.execute(select(Book).where(Book.book_id == book_id))
            book = result.scalars().first()
            if not book:
                raise ResourceNotFoundException(f"Book with ID {book_id} does not exist")
            return BookRead.model_validate(book)






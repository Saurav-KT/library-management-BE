from sqlalchemy import delete, false, and_
from sqlalchemy.orm import selectinload
from sqlmodel import select, func
from app.core.exception import ResourceNotFoundException, ValidationException
from app.models.book import Book
from app.models.bookcopy import BookCopy
from app.schemas.book_schema import BookCreate, BookRead, BookReadWithRelations, BookUpdate
from app.service.base_service import BaseService
from app.utils.base_enum import Status, Location

class BookService(BaseService):

    async def create_book(self, book_data: BookCreate) -> BookRead:
            # Create an ORM object
            async with self.session.begin():
                new_book = Book(**book_data.model_dump())
                self.session.add(new_book)
                await self.session.flush()
                #  Create copies
                copies = [
                    BookCopy(book_id=new_book.book_id,status=Status.AVAILABLE, location=Location.SHELF)
                    for _ in range(new_book.total_copies)
                ]

                self.session.add_all(copies)
            await self.refresh(new_book)

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
        async with self.session.begin():
            update_data=book_obj.model_dump(exclude_unset=True)
            if not update_data:
                raise ValidationException("No fields provided for update")
            result = await self.session.execute(select(Book).where(Book.book_id == book_id))
            book = result.scalar_one_or_none()
            if not book:
                raise ResourceNotFoundException(f"Book with ID {book_id} does not exist")

            if "total_copies" in update_data:
                await self.sync_copies(book_id,old_total= book.total_copies, new_total=update_data["total_copies"])

            # Update book
            book.sqlmodel_update(update_data)
            self.session.add(book)

        await self.refresh(book)
        # Return updated DB object
        return BookRead.model_validate(book)

    async def delete_book(self, book_id: int):
        async with self.session.begin():
            result = await self.session.execute(select(Book).where(Book.book_id == book_id))
            book = result.scalar_one_or_none()
            if not book:
                raise ResourceNotFoundException(f"Book with ID {book_id} does not exist")

            issued_count = await self.session.scalar(
                select(func.count()).where(BookCopy.book_id == book_id, BookCopy.status == Status.ISSUED))

            if issued_count > 0:
                raise ValidationException(
                    f"Cannot delete book. {issued_count} copies are issued"
                )
            #  Delete copies
            await self.session.execute(delete(BookCopy).where(and_(BookCopy.book_id == book_id,
                                                                   BookCopy.status == Status.AVAILABLE))
                )
            # Delete book
            await self.session.delete(book)



    async def sync_copies(self, book_id: int,old_total: int, new_total: int):
        """
        Sync book_copies table with updated total_copies.
        Handles:
            - Increasing copies (insert)
            - Decreasing copies (delete available only)
            - Validation (issued copies constraint)
            """

        issued_count= await self.session.scalar(select(func.count()).where(BookCopy.book_id== book_id, BookCopy.status==Status.ISSUED))
        if new_total < issued_count:
            raise ValidationException("Total copies cannot be reduced below issued books")

            # CASE 1: INCREASE COPIES
        if new_total > old_total:
           difference = new_total - old_total
           new_copies = [
                BookCopy(book_id=book_id, status=Status.AVAILABLE, location= Location.SHELF)
                for _ in range(difference)
                ]
           self.session.add_all(new_copies)

        # CASE 2: DECREASE COPIES
        elif new_total < old_total:
           difference = old_total - new_total

           # Fetch removable copies
           result = await self.session.execute(
               select(BookCopy.copy_id)
               .where(
                   BookCopy.book_id == book_id,
                   BookCopy.status == Status.AVAILABLE
               )
               .order_by(BookCopy.copy_id)
               .limit(difference)
               .with_for_update() # handle concurrent scenario
           )

           # Prevent deleting more AVAILABLE copies than exist
           removable_copies = result.scalars().all()
           if len(removable_copies) < difference:
               raise ValidationException(f"Cannot remove {difference} copies. Only {len(removable_copies)} available.")

          # Delete book copies
           condition = (
               BookCopy.copy_id.in_(removable_copies)
               if removable_copies
               else false()
           )
           await self.session.execute(
               delete(BookCopy).where(condition)
           )
           # await self.session.execute(
           #      delete(BookCopy).where(
           #          and_(
           #              BookCopy.copy_id.in_(removable_copies),
           #              BookCopy.status == Status.AVAILABLE
           #          )
           #      )
           #  )






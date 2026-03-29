from fastapi import APIRouter, status, Depends, HTTPException
from app.schemas.book_schema import BookCreate, BookRead, BookReadWithRelations, BookUpdate
from app.utils.response import success_response, SuccessResponse
from app.service.book_service import BookService
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.database import get_db
from app.utils.message import build_message

router = APIRouter(
    prefix="/books",
    tags=["Books"]
)

@router.post("", response_model=SuccessResponse[BookRead])
async def create_book(book: BookCreate, session: AsyncSession = Depends(get_db)):
        service = BookService(session)
        book_obj = await service.create_book(book)
        if book_obj:
            return success_response(build_message("create", "Book"), data= book_obj,
                                    status_code=status.HTTP_201_CREATED)

@router.patch("/{book_id}", response_model=SuccessResponse[BookRead])
async def update_book(book_id: int, book: BookUpdate, session: AsyncSession = Depends(get_db)):
    service = BookService(session)
    updated_book= await service.update_book(book_id=book_id, book_obj=book)
    return success_response(build_message("update", "Book"), data=updated_book,
                                status_code=status.HTTP_200_OK)

@router.delete("/{book_id}")
async def delete_book(book_id: int, session: AsyncSession= Depends(get_db)):
    service = BookService(session)
    await service.delete_book(book_id=book_id)
    return success_response(build_message("delete", "Book"),status_code=status.HTTP_200_OK)


@router.get("",response_model=SuccessResponse[list[BookReadWithRelations]])
async def get_all(session: AsyncSession = Depends(get_db)):
    service= BookService(session)
    books = await service.get_books()
    return success_response(build_message("list", "Books", len(books)), data=books,
                                status_code=status.HTTP_200_OK)

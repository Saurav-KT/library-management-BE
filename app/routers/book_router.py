from fastapi import APIRouter, status, Depends, HTTPException
from app.schemas.book_schema import BookCreate, BookRead
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



# @router.get("/{book_id}", response_model=BookRead)
# def get_book(book_id: int, session: Session = Depends(get_session)):
#     order = get_order(order_number, customer_id)
#
#     return success_response(
#         data=order,
#         status_code=status.HTTP_200_OK
#     )
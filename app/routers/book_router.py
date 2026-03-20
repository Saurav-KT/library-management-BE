from fastapi import APIRouter, status, Depends, HTTPException
from app.schemas.book_schema import BookCreate, BookRead
from app.utils.response import success_response, SuccessResponse
from app.service.book_service import BookService
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.database import get_db

router = APIRouter(
    prefix="/books",
    tags=["Books"]
)


@router.post("", response_model=SuccessResponse[BookRead])
async def create_book(book: BookCreate, session: AsyncSession = Depends(get_db)):
    try:

        book_obj = await BookService.create_book (book, session)
        if book_obj:
            return success_response("Book created successfully", data= book_obj,
                                    status_code=status.HTTP_201_CREATED)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

# @router.get("/{book_id}", response_model=BookRead)
# def get_book(book_id: int, session: Session = Depends(get_session)):
#     order = get_order(order_number, customer_id)
#
#     return success_response(
#         data=order,
#         status_code=status.HTTP_200_OK
#     )


# @router.delete("/{order_number}/{customer_id}", response_model=SuccessResponse)
# async def delete_purchase_order(order_number: str, customer_id: int):
#     delete_order(order_number,customer_id)
#
#     return success_response(
#         message="Order deleted successfully",
#         status_code=status.HTTP_200_OK
#     )
#
# @router.put("/{order_number}/{customer_id}")
# async def update_purchase_order(order_number:str, customer_id: int, payload: OrderUpdateRequest):
#     update_order(order_number,customer_id,payload)
#     return success_response(
#         message="Order updated successfully",
#         status_code=status.HTTP_200_OK
#     )

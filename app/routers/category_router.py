from fastapi import Depends, APIRouter, status
from app.schemas.category_schema import CategoryRead
from app.utils.response import success_response, SuccessResponse
from app.service.category_service import CategoryService
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.database import get_db
from app.utils.message import build_message

router = APIRouter(
    prefix="/categories",
    tags=["Categories"]
)


@router.get("", response_model=SuccessResponse[list[CategoryRead]])
async def get_all_categories(session: AsyncSession = Depends(get_db)):
    service = CategoryService(session)
    categories = await service.get_all_category()
    return success_response(build_message("list", "Category", len(categories)), data=categories,
                            status_code=status.HTTP_200_OK)

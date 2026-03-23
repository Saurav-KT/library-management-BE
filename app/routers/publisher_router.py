from fastapi import Depends, APIRouter, status
from app.schemas.category_schema import CategoryRead
from app.utils.response import success_response, SuccessResponse
from app.service.publisher_service import PublisherService
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.database import get_db
from app.utils.message import build_message

router = APIRouter(
    prefix="/publishers",
    tags=["publishers"]
)

@router.get("",response_model=SuccessResponse[list[CategoryRead]])
async def get_all_publisher(session: AsyncSession = Depends(get_db)):
    service= PublisherService(session)
    publishers = await service.get_all_publisher()
    if publishers:
        return success_response(build_message("list", "Publisher", len(publishers)), data=publishers,
                                status_code=status.HTTP_200_OK)
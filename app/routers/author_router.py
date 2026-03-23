from fastapi import Depends, APIRouter, status
from app.schemas.author_schema import AuthorRead
from app.utils.response import success_response, SuccessResponse
from app.service.author_service import AuthorService
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.database import get_db
from app.utils.message import build_message

router = APIRouter(
    prefix="/authors",
    tags=["Authors"]
)

@router.get("",response_model=SuccessResponse[list[AuthorRead]])
async def get_all_author(session: AsyncSession = Depends(get_db)):
    service= AuthorService(session)
    categories = await service.get_all_author()
    if categories:
        return success_response(build_message("list", "Author", len(categories)), data=categories,
                                status_code=status.HTTP_200_OK)
from fastapi import APIRouter, status, Depends, HTTPException
from app.schemas.member_schema import MemberCreate, MemberRead, MemberUpdate
from app.utils.response import success_response, SuccessResponse
from app.service.member_service import MemberService
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.database import get_db
from app.utils.message import build_message

router = APIRouter(
    prefix="/members",
    tags=["Members"]
)

@router.post("", response_model=SuccessResponse[MemberRead])
async def create_book(member: MemberCreate, session: AsyncSession = Depends(get_db)):
        service = MemberService(session)
        member_obj = await service.create_member(member)
        if member_obj:
            return success_response(build_message("create", "Member"), data= member_obj,
                                    status_code=status.HTTP_201_CREATED)
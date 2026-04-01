from datetime import datetime, timezone
from sqlmodel import Field, Relationship
from app.models.base import BaseModel
from app.utils.base_enum import MemberType
from typing import List
from app.utils.base_enum import MemberStatus

class Member(BaseModel, table=True):
    __tablename__ = "member"

    member_id: int = Field(default=None, primary_key=True)
    name: str=Field(index=True, nullable=False)
    email: str = Field(unique=True, nullable=False)
    phone: str= Field(nullable= False)
    address: str | None = Field(nullable= True)
    membership_date: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    membership_type: MemberType = Field(default=MemberType.STUDENT)
    member_status: MemberStatus = Field(default=MemberStatus.ACTIVE)

    borrows: List["Borrow"] = Relationship(back_populates="member")
    fines: List["Fine"] = Relationship(back_populates="member")
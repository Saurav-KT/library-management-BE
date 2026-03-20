from datetime import date
from sqlmodel import Field, Relationship
from app.models.base import BaseModel
from app.utils.base_enum import MemberType
from typing import List

class Member(BaseModel, table=True):
    __tablename__ = "member"

    member_id: int = Field(default=None, primary_key=True)
    name: str
    email: str
    phone: str = None
    address: str | None = None
    membership_date: date | None = None
    membership_type: MemberType = Field(default=MemberType.STUDENT)
    status: str | None = "active"

    borrows: List["Borrow"] = Relationship(back_populates="member")
    fines: List["Fine"] = Relationship(back_populates="member")
from pydantic import BaseModel, Field, ConfigDict, EmailStr, StringConstraints
from datetime import datetime, timezone
from app.utils.base_enum import MemberType, MemberStatus
from typing import Annotated

NameStr = Annotated[str, StringConstraints(min_length=3, max_length=50)]
PhoneStr = Annotated[str, StringConstraints(pattern=r"^[0-9]{10}$")]

class MemberBase(BaseModel):
    name: NameStr
    email: EmailStr
    phone: PhoneStr
    address: str | None = None
    membership_date:datetime= Field(default_factory=lambda: datetime.now(timezone.utc))
    membership_type: MemberType = Field(default=MemberType.STUDENT)
    status: MemberStatus = MemberStatus.ACTIVE

class MemberRead(MemberBase):
    member_id: int
    model_config = ConfigDict(from_attributes=True)


class MemberCreate(MemberBase):
    pass


class MemberUpdate(MemberBase):
  pass


class MemberDelete:
    member_id: int

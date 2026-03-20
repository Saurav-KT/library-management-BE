from typing import Optional
from datetime import date
from sqlmodel import  Field, Relationship
from app.models.base import BaseModel

class Fine(BaseModel, table=True):
    fine_id: int = Field(default=None, primary_key=True)
    member_id: int = Field(foreign_key="member.member_id")
    borrow_id: int| None = Field(foreign_key="borrow.borrow_id")
    amount: float
    reason: str | None = None  # late return, lost book, damaged
    paid: bool = False
    date_issued: date | None = None
    date_paid: date | None = None

    member: Optional["Member"] = Relationship(back_populates="fines")
    borrow: Optional["Borrow"] = Relationship()
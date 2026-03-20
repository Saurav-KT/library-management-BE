from sqlmodel import Field
from app.models.base import BaseModel

class Staff(BaseModel, table=True):
    staff_id: int = Field(default=None, primary_key=True)
    name: str= Field(nullable=False)
    email: str= Field(nullable=False)
    phone: str= Field(nullable=False)
    password_hash: str = Field(nullable=False)
    role: str = "Librarian"
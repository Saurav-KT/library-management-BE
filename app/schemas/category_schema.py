from pydantic import BaseModel

class CategoryRead(BaseModel):
    category_id: int
    category_name: str
    description: str | None= None
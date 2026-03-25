from pydantic import BaseModel

class AuthorRead(BaseModel):
    author_id: int
    author_name: str
    country: str | None = None

    model_config = {"from_attributes": True}
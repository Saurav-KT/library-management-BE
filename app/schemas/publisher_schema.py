from pydantic import BaseModel

class PublisherRead(BaseModel):
    publisher_id: int
    publisher_name: str
    address: str | None = None
    phone: int | None = None

    model_config = {"from_attributes": True}
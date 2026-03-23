from pydantic import BaseModel

class PublisherRead(BaseModel):
    publisher_id: int
    publisher_name: str
    address: str | None = None
    phone: str | None = None
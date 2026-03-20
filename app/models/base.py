from sqlmodel import MetaData
from sqlmodel import SQLModel
from app.settings.config import SCHEMA

class BaseModel(SQLModel):
    metadata = MetaData(schema= SCHEMA)
    SQLModel.metadata = metadata
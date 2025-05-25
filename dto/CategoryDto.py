import uuid
from pydantic import BaseModel

class CategoryDto(BaseModel):
    id: int
    name: str
    transactionUuids: list[uuid.UUID]
    
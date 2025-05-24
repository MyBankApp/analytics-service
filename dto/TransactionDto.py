import uuid
from datetime import datetime
from decimal import Decimal
from pydantic import BaseModel
from enums.Currency import Currency
from enums.Status import Status

class TransactionDto(BaseModel):
    id: uuid.UUID 
    amount: Decimal
    currency: Currency
    status: Status
    createdAt: datetime
    description: str
    senderId: int
    receiverId: int
    categoryId: int
    
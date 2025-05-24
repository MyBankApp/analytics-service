from fastapi import APIRouter
from dto.TransactionDto import TransactionDto
from service.transactionService import service

transaction_controller = APIRouter()

@transaction_controller.get("/analyze/transactions/{sender_id}")
async def get_transactions_by_sender_id(sender_id: int):
    return await service.get_transactions_by_sender_id(sender_id)

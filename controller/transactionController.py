from fastapi import APIRouter
from service.transactionService import service

transaction_controller = APIRouter()

@transaction_controller.get("/{sender_id}")
async def get_transactions_by_sender_id(sender_id: int):
    return await service.get_transactions_by_sender_id(sender_id)

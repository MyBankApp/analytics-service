from fastapi import APIRouter
from controller.transactionController import transaction_controller

api_router = APIRouter(prefix="/api")

api_router.include_router(transaction_controller)
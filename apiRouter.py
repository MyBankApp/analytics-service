from fastapi import APIRouter
from controller.transactionController import transaction_controller
from controller.analyticController import analytic_controller

api_router = APIRouter(prefix="/api")

api_router.include_router(transaction_controller, prefix="/transactions")
api_router.include_router(analytic_controller, prefix="/analytic")
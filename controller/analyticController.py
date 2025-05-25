from fastapi import APIRouter
from service.analyticService import service

analytic_controller = APIRouter()

@analytic_controller.get("/category/{sender_id}")
async def category_distribution(sender_id: int):
    return await service.category_distribution(sender_id)
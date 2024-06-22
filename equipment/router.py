from fastapi import APIRouter, Depends
from auth.utils import jwt_auth
from equipment.models import Equipment
from utils.database import equipment

equipment_router = APIRouter(tags=['equipment'], prefix='/equipment')

@equipment_router.get("/list")
async def get_equipment_list(user: dict = Depends(jwt_auth.login_required)) -> list:
    return await equipment.get_equipment_list()

@equipment_router.post("/add")
async def add_equipment(equipment_data: Equipment, user: dict = Depends(jwt_auth.login_required)) -> dict:
    return await equipment.insert_equipment(equipment_data.ip_address, equipment_data.name)

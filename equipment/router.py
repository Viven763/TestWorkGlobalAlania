from fastapi import APIRouter, Depends, WebSocket, WebSocketDisconnect, WebSocketException
from websockets.exceptions import ConnectionClosed
import asyncio
from auth.utils import jwt_auth
from equipment.models import Equipment
from utils.database import equipment

equipment_router = APIRouter(tags=['equipment'], prefix='/equipment')

@equipment_router.get("/list")
async def get_equipment_list(user: dict = Depends(jwt_auth.login_required)) -> list:
    return await equipment.get_equipment_list()

@equipment_router.websocket("/ws/list")
async def websocket_list(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            data = await equipment.get_equipment_list()
            await websocket.send_json(data)
            await asyncio.sleep(1)
    except (WebSocketDisconnect, ConnectionClosed, WebSocketException):
        await websocket.close()
@equipment_router.post("/add")
async def add_equipment(equipment_data: Equipment, user: dict = Depends(jwt_auth.login_required)) -> dict:
    return await equipment.insert_equipment(equipment_data.ip_address, equipment_data.name)

@equipment_router.delete("/delete")
async def delete_equipment(uuid: str, user: dict = Depends(jwt_auth.login_required)) -> dict:
    return await equipment.delete_equipment(uuid)
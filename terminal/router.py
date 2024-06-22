from fastapi import APIRouter, Depends
from auth.utils import jwt_auth
from terminal.models import Terminal
from utils.database import terminal

terminal_router = APIRouter(tags=['terminal'], prefix='/terminal')

@terminal_router.post('/add')
async def add_terminal(terminal_data: Terminal, user: dict = Depends(jwt_auth.login_required)) -> dict:
    return await terminal.add_terminal(terminal_data.device_uuid, terminal_data.mac_address, terminal_data.model)

@terminal_router.delete('/delete')
async def delete_terminal(terminal_uuid: str, user: dict = Depends(jwt_auth.login_required)) -> dict:
    return await terminal.delete_terminal(terminal_uuid)
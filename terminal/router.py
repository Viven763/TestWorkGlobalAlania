from fastapi import APIRouter, Depends, WebSocket, WebSocketException, WebSocketDisconnect
from websockets.exceptions import ConnectionClosed
import asyncio
from auth.utils import jwt_auth
from terminal.models import Terminal
from utils.database import terminal

terminal_router = APIRouter(tags=['terminal'], prefix='/terminal')

@terminal_router.get('/list')
async def list_terminals(user: dict = Depends(jwt_auth.login_required)) -> list:
    return await terminal.get_terminal_list()

@terminal_router.websocket('/ws/list')
async def websocket_list(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            data = await terminal.get_terminal_list()
            await websocket.send_json(data)
            await asyncio.sleep(1)
    except (ConnectionClosed, WebSocketDisconnect, WebSocketException):
        await websocket.close()

@terminal_router.post('/add')
async def add_terminal(terminal_data: Terminal, user: dict = Depends(jwt_auth.login_required)) -> dict:
    return await terminal.add_terminal(terminal_data.device_uuid, terminal_data.mac_address, terminal_data.model)

@terminal_router.delete('/delete')
async def delete_terminal(terminal_uuid: str, user: dict = Depends(jwt_auth.login_required)) -> dict:
    return await terminal.delete_terminal(terminal_uuid)
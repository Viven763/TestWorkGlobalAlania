from fastapi import APIRouter, Depends
from auth.utils import jwt_auth
from utils.database import users
import bcrypt
from users.models import Register, PatchUserData

users_router = APIRouter(tags=['users'], prefix='/users')

@users_router.get('/list')
async def list_users(user: dict = Depends(jwt_auth.login_required)) -> list:
    return await users.get_users_list()

@users_router.post('/register')
async def register(user: Register) -> dict:
    hashed_password = bcrypt.hashpw(user.password.encode('utf-8'), bcrypt.gensalt())
    user.password = hashed_password.decode('utf-8')
    return await users.register_user(user.login, user.password, user.fio)

@users_router.post('/add')
async def create_user(register: Register, user: dict = Depends(jwt_auth.login_required)) -> dict:
    return await users.register_user(register.login, register.password, register.fio)

@users_router.patch('/update')
async def update_user_data(patch_data: PatchUserData, user: dict = Depends(jwt_auth.login_required)) -> dict:
    return await users.update_user_data(user['uuid'], patch_data.fio)

@users_router.delete('/delete')
async def delete_user(user_id: str, user: dict = Depends(jwt_auth.login_required)) -> dict:
    return await users.delete_user(user_id)
from fastapi import APIRouter, Depends
from auth.utils import jwt_auth
from utils.database import users

login_router = APIRouter(tags=['login'])

@login_router.post('/auth')
def login(token: str = Depends(jwt_auth.login_user)) -> dict:
    return {"status": "ok", "access_token": f"Bearer {token}"}
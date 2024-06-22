from fastapi import HTTPException, Security, Depends
from auth.models import Auth
from fastapi_jwt import JwtAccessBearer, JwtAuthorizationCredentials
from utils.database import users, auth
from datetime import datetime, timedelta
import os
import bcrypt

secret_key = os.environ.get("SECRET_KEY")
security = JwtAccessBearer(secret_key=secret_key, auto_error=False)

async def login_user(user: Auth) -> str:
    user_data = await users.get_current_user(user.login)
    if user_data is None or not bcrypt.checkpw(user.password.encode('utf-8'), user_data['password'].encode('utf-8')):
        raise HTTPException(status_code=403,
                             detail="Incorrect username or password",
                             headers={"WWW-Authenticate": "Bearer"})
    current_date = datetime.now()
    expires = timedelta(days=1)
    expires_date = current_date + expires
    access_token = security.create_access_token(user_data, expires)
    await auth.insert_token(user_data['uuid'], access_token, expires_date)
    return access_token

def get_current_user(token: JwtAuthorizationCredentials = Security(security)):
    if token is None:
        raise HTTPException(status_code=403,
                             detail="Incorrect or empty auth token",
                             headers={'WWW-Authenticate': 'Bearer'})
    return token.subject

def login_required(user: Auth = Depends(get_current_user)) -> Auth:
    if user is None:
        raise HTTPException(status_code=403,
                             detail="Incorrect username or password",
                             headers={'WWW-Authenticate': 'Bearer'})
    return user
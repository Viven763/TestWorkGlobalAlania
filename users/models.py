from pydantic import BaseModel

class PatchUserData(BaseModel):
    fio: str

class Register(BaseModel):
    login: str
    password: str
    fio: str
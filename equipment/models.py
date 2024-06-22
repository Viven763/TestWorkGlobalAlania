from pydantic import BaseModel

class Equipment(BaseModel):
    ip_address: str
    name: str
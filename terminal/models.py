from pydantic import BaseModel

class Terminal(BaseModel):
    device_uuid: str
    mac_address: str
    model: str
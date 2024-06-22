import asyncpg
import uuid
from datetime import datetime

async def add_terminal(device_uuid: str, mac_address: str, model: str) -> dict:
    conn = await asyncpg.connect()
    try:
        await conn.execute("INSERT INTO terminal_list VALUES($1, $2, $3, $4, $5)",
                           uuid.uuid4(), uuid.UUID(device_uuid), mac_address, model, datetime.now())
        return {"message": "success"}
    except ValueError:
        return {"error": "incorrect UUID"}
    except asyncpg.exceptions.ForeignKeyViolationError:
        return {"error": "incorrect device_uuid"}
    finally:
        await conn.close()

async def get_terminal_list() -> list:
    conn = await asyncpg.connect()
    try:
        data = await conn.fetch("SELECT * FROM terminal_list")
        json_data = [{
            "uuid": str(terminal['uuid']),
            "device_uuid": str(terminal['device_uuid']),
            "mac_address": terminal['mac'],
            "model": terminal['model'],
            "create_date": terminal['dt_created'],
            "last_pool_date": terminal['dt_last_pool']
        } for terminal in data]
        return json_data
    finally:
        await conn.close()

async def delete_terminal(terminal_uuid: str) -> dict:
    conn = await asyncpg.connect()
    try:
        data = await conn.execute("DELETE FROM terminal_list WHERE uuid = $1",
                           uuid.UUID(terminal_uuid))
        if int(data.split(" ")[-1]) == 0:
            return {"error": "terminal does not exist"}
        return {"message": "success"}
    except ValueError:
        return {"error": "incorrect UUID"}
    finally:
        await conn.close()
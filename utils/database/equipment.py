import asyncpg
import uuid

async def insert_equipment(ip_address: str, desc: str) -> dict:
    conn = await asyncpg.connect()
    try:
        await conn.execute("INSERT INTO equipment_list VALUES ($1, $2, $3)",
                           uuid.uuid4(), ip_address, desc)
        return {"message": "success"}
    finally:
        await conn.close()

async def delete_equipment(equipment_uuid: str) -> dict:
    conn = await asyncpg.connect()
    try:
        await conn.execute("DELETE FROM terminal_list WHERE device_uuid = $1",
                           uuid.UUID(equipment_uuid))
        data = await conn.execute("DELETE FROM equipment_list WHERE uuid = $1",
                                  uuid.UUID(equipment_uuid))
        if int(data.split(" ")[-1]) == 0:
            return {"error": "equipment not found"}
        return {"message": "success"}
    except ValueError:
        return {"error": "incorrect UUID"}
    finally:
        await conn.close()
async def get_equipment_list() -> list:
    conn = await asyncpg.connect()
    try:
        data = await conn.fetch("SELECT * FROM equipment_list")
        json_data = [{
            "uuid": str(equipment['uuid']),
            "ip_address": equipment['ip_address'],
            "desc": equipment['description']
        } for equipment in data]
        return json_data
    finally:
        await conn.close()


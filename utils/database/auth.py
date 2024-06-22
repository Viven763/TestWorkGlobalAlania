import asyncpg
from datetime import datetime
import uuid

async def insert_token(user_uuid: uuid, access_token: str, expires: datetime):
    conn = await asyncpg.connect()
    try:
        await conn.execute("INSERT INTO auth VALUES ($1, $2, $3, $4)",
                           uuid.uuid4(), uuid.UUID(user_uuid), access_token, expires)
    finally:
        await conn.close()
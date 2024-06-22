import asyncpg
import uuid

async def get_current_user(username) -> dict | None:
    conn = await asyncpg.connect()
    try:
        data = await conn.fetchrow("SELECT * FROM users WHERE login = $1",
                              username)
        if data is None:
            return None
        json_data = {
            "uuid": str(data['uuid']),
            "password": data['pswd'],
            "login": data['login'],
            "fio": data['fio'],
            "status": data['status']
        }
        return json_data
    finally:
        await conn.close()

async def register_user(username: str, password: str, fio: str) -> dict:
    conn = await asyncpg.connect()
    try:
        await conn.execute("INSERT INTO users VALUES($1, $2, $3, $4, $5)",
                           uuid.uuid4(), username, password, fio, 0)
        return {"message": "success"}
    except asyncpg.exceptions.UniqueViolationError:
        return {"error": "user already exists"}
    finally:
        await conn.close()

async def get_users_list() -> list:
    conn = await asyncpg.connect()
    try:
        data = await conn.fetch("SELECT * FROM users")
        json_data = [{
            "uuid": str(user['uuid']),
            "login": user['login'],
            "fio": user['fio'],
            "status": user['status']
        } for user in data]
        return json_data
    finally:
        await conn.close()

async def update_user_data(user_uuid: uuid, fio: str) -> dict:
    conn = await asyncpg.connect()
    try:
        await conn.execute("UPDATE users SET fio = $1 WHERE uuid = $2",
                           fio, user_uuid)
        return {"message": "success"}
    finally:
        await conn.close()

async def delete_user(user_uuid) -> dict:
    conn = await asyncpg.connect()
    try:
        data = await conn.execute("DELETE FROM users WHERE uuid = $1",
                           uuid.UUID(user_uuid))
        if int(data.split(" ")[-1]) == 0:
            return {"error": "user not found"}
        return {"message": "success"}
    except ValueError:
        return {"error": "incorrect UUID"}
    finally:
        await conn.close()
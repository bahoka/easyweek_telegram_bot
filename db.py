import asyncpg
import os
from dotenv import load_dotenv

load_dotenv()
DB_URL = os.getenv("DATABASE_URL")

async def init_db():
    conn = await asyncpg.connect(DB_URL)
    await conn.execute('''
        CREATE TABLE IF NOT EXISTS users (
            phone TEXT PRIMARY KEY,
            chat_id BIGINT
        )
    ''')
    await conn.close()

async def save_user(phone, chat_id):
    conn = await asyncpg.connect(DB_URL)
    await conn.execute('''
        INSERT INTO users (phone, chat_id)
        VALUES ($1, $2)
        ON CONFLICT (phone) DO UPDATE SET chat_id = EXCLUDED.chat_id
    ''', phone, chat_id)
    await conn.close()

async def get_chat_id_by_phone(phone):
    conn = await asyncpg.connect(DB_URL)
    row = await conn.fetchrow('SELECT chat_id FROM users WHERE phone = $1', phone)
    await conn.close()
    return row['chat_id'] if row else None

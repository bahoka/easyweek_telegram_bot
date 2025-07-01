import sqlite3

DB_NAME = 'users.db'

def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            phone TEXT PRIMARY KEY,
            chat_id INTEGER
        )
    ''')
    conn.commit()
    conn.close()

def save_user(phone, chat_id):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('REPLACE INTO users (phone, chat_id) VALUES (?, ?)', (phone, chat_id))
    conn.commit()
    conn.close()

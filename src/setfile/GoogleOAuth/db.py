import sqlite3
from pathlib import Path

db_path = Path(__file__).resolve().parent.parent.parent.parent/'data/setfile.db'

def get_db():
    return sqlite3.connect(db_path)

def init_db():
    db = get_db()
    db.execute( """
    CREATE TABLE IF NOT EXISTS users (
    google_id TEXT PRIMARY KEY,
    email TEXT,
    refresh_token TEXT,
    access_token TEXT,
    expires_at TEXT
    )
    """
    )
    db.commit()
    db.close()
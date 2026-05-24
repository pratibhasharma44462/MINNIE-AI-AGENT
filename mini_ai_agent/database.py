import sqlite3
import os
from datetime import datetime

DB_PATH = "minnie.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.execute("""
        CREATE TABLE IF NOT EXISTS sessions (
            id         INTEGER PRIMARY KEY AUTOINCREMENT,
            session_id TEXT    UNIQUE NOT NULL,
            created_at TEXT    NOT NULL
        )
    """)

    c.execute("""
        CREATE TABLE IF NOT EXISTS messages (
            id         INTEGER PRIMARY KEY AUTOINCREMENT,
            session_id TEXT NOT NULL,
            role       TEXT NOT NULL,      -- 'user' or 'assistant'
            content    TEXT NOT NULL,
            timestamp  TEXT NOT NULL,
            FOREIGN KEY (session_id) REFERENCES sessions(session_id)
        )
    """)

    conn.commit()
    conn.close()


def create_session(session_id: str):
    conn = sqlite3.connect(DB_PATH)
    c    = conn.cursor()
    c.execute("""
        INSERT OR IGNORE INTO sessions (session_id, created_at)
        VALUES (?, ?)
    """, (session_id, datetime.now().isoformat()))
    conn.commit()
    conn.close()


def save_message(session_id: str, role: str, content: str):
    conn = sqlite3.connect(DB_PATH)
    c    = conn.cursor()
    c.execute("""
        INSERT INTO messages (session_id, role, content, timestamp)
        VALUES (?, ?, ?, ?)
    """, (session_id, role, content, datetime.now().isoformat()))
    conn.commit()
    conn.close()


def get_history(session_id: str) -> list:
    conn = sqlite3.connect(DB_PATH)
    c    = conn.cursor()
    c.execute("""
        SELECT role, content FROM messages
        WHERE session_id = ?
        ORDER BY timestamp ASC
    """, (session_id,))
    rows = c.fetchall()
    conn.close()
    return [{"role": row[0], "content": row[1]} for row in rows]


def get_all_sessions() -> list:
    conn = sqlite3.connect(DB_PATH)
    c    = conn.cursor()
    c.execute("""
        SELECT session_id, created_at FROM sessions
        ORDER BY created_at DESC
    """)
    rows = c.fetchall()
    conn.close()
    return [{"session_id": row[0], "created_at": row[1]} for row in rows]


def clear_session(session_id: str):
    conn = sqlite3.connect(DB_PATH)
    c    = conn.cursor()
    c.execute("DELETE FROM messages WHERE session_id = ?", (session_id,))
    conn.commit()
    conn.close()

import sqlite3
import json
from datetime import datetime
from typing import Optional, List, Dict, Any
from pathlib import Path

class DatabaseManager:
    def __init__(self, storybase: str = "default"):
        self.db_dir = Path("db")
        self.db_dir.mkdir(exist_ok=True)
        
        # If storybase ends with .db, use it as is, otherwise append .db
        if storybase.endswith(".db"):
             self.db_path = self.db_dir / storybase
        else:
             self.db_path = self.db_dir / f"{storybase}.db"
             
        self._init_db()

    def _get_connection(self):
        conn = sqlite3.connect(str(self.db_path))
        conn.row_factory = sqlite3.Row
        return conn

    def _init_db(self):
        conn = self._get_connection()
        cursor = conn.cursor()
        
        # Stories table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS stories (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                summary TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')

        # Characters table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS characters (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                story_id INTEGER,
                name TEXT NOT NULL,
                data JSON,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (story_id) REFERENCES stories (id)
            )
        ''')

        # Events table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS events (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                story_id INTEGER,
                description TEXT NOT NULL,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (story_id) REFERENCES stories (id)
            )
        ''')

        # Inventory table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS inventory (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                story_id INTEGER,
                owner_id INTEGER,
                item_name TEXT NOT NULL,
                details JSON,
                FOREIGN KEY (story_id) REFERENCES stories (id),
                FOREIGN KEY (owner_id) REFERENCES characters (id)
            )
        ''')

        # World State table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS world_state (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                story_id INTEGER,
                key TEXT NOT NULL,
                value TEXT,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (story_id) REFERENCES stories (id),
                UNIQUE(story_id, key)
            )
        ''')

        # Campaigns table (for template distribution)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS campaigns (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                description TEXT,
                lore_prefix TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        conn.commit()
        conn.close()

    def create_story(self, name: str, summary: str = "") -> int:
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO stories (name, summary) VALUES (?, ?)",
            (name, summary)
        )
        story_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return story_id

    def get_story(self, story_id: int) -> Optional[Dict[str, Any]]:
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM stories WHERE id = ?", (story_id,))
        row = cursor.fetchone()
        conn.close()
        return dict(row) if row else None

    def update_story_summary(self, story_id: int, summary: str):
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE stories SET summary = ?, updated_at = CURRENT_TIMESTAMP WHERE id = ?",
            (summary, story_id)
        )
        conn.commit()
        conn.close()

    def add_character(self, story_id: int, name: str, data: Dict[str, Any]) -> int:
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO characters (story_id, name, data) VALUES (?, ?, ?)",
            (story_id, name, json.dumps(data))
        )
        char_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return char_id

    def get_characters(self, story_id: int) -> List[Dict[str, Any]]:
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM characters WHERE story_id = ?", (story_id,))
        rows = cursor.fetchall()
        conn.close()
        return [dict(row) for row in rows]

    def log_event(self, story_id: int, description: str):
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO events (story_id, description) VALUES (?, ?)",
            (story_id, description)
        )
        conn.commit()
        conn.close()

    def get_recent_events(self, story_id: int, limit: int = 10) -> List[Dict[str, Any]]:
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT * FROM events WHERE story_id = ? ORDER BY timestamp DESC LIMIT ?",
            (story_id, limit)
        )
        rows = cursor.fetchall()
        conn.close()
        return [dict(row) for row in rows][::-1]

    def set_world_state(self, story_id: int, key: str, value: str):
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO world_state (story_id, key, value) VALUES (?, ?, ?) ON CONFLICT(story_id, key) DO UPDATE SET value = ?, updated_at = CURRENT_TIMESTAMP",
            (story_id, key, value, value)
        )
        conn.commit()
        conn.close()

    def get_world_state(self, story_id: int) -> Dict[str, str]:
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT key, value FROM world_state WHERE story_id = ?", (story_id,))
        rows = cursor.fetchall()
        conn.close()
        return {row['key']: row['value'] for row in rows}

    def create_campaign(self, name: str, description: str, lore_prefix: str) -> int:
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO campaigns (name, description, lore_prefix) VALUES (?, ?, ?)",
            (name, description, lore_prefix)
        )
        campaign_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return campaign_id

    def list_campaigns(self) -> List[Dict[str, Any]]:
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM campaigns")
        rows = cursor.fetchall()
        conn.close()
        return [dict(row) for row in rows]

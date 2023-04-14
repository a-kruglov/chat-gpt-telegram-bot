import sqlite3
import telebot
import config
from typing import List


class MessageDataBase:
    def __init__(self, db_path):
        self.db_path = db_path
        self._init_db()

    def _init_db(self):
        conn = sqlite3.connect(self.db_path)
        conn.execute(
            "CREATE TABLE IF NOT EXISTS messages (chat_id INTEGER, role TEXT, content TEXT, timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP)")
        conn.execute("CREATE TABLE IF NOT EXISTS whitelist (chat_id INTEGER)")
        conn.close()

    def get_messages_amount_for_user_in_this_month(self, message: telebot.types.Message):
        chat_id = message.chat.id
        query = """SELECT COUNT(*) FROM messages WHERE chat_id = ? AND role = 'user' 
                   AND strftime('%m', timestamp) = strftime('%m', 'now')"""
        conn = sqlite3.connect(self.db_path)
        count = conn.execute(query, (chat_id,)).fetchone()[0]
        conn.close()
        return count

    def store_message(self, text: str, context_message: telebot.types.Message):
        chat_id = context_message.chat.id
        if context_message.from_user.username == config.BOT_USERNAME:
            role = "assistant"
            content = text
        else:
            role = "user"
            name = context_message.from_user.username or f"{context_message.from_user.first_name} {context_message.from_user.last_name}"
            if context_message.chat.type == "group":
                content = f'[{name}]: {text}'
            else:
                content = text

        query = "INSERT INTO messages (chat_id, role, content) VALUES (?, ?, ?)"
        conn = sqlite3.connect(self.db_path)
        conn.execute(query, (chat_id, role, content))
        conn.commit()
        conn.close()

    def get_recent_messages(self, chat_id: int, limit: int) -> List[dict]:
        query = "SELECT role, content FROM messages WHERE chat_id = ? ORDER BY timestamp DESC LIMIT ?"
        conn = sqlite3.connect(self.db_path)
        rows = conn.execute(query, (chat_id, limit)).fetchall()
        messages = [{"role": row[0], "content": row[1]} for row in rows]
        conn.close()
        return messages[::-1]

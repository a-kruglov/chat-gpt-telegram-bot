import sqlite3
import telebot


class Whitelist:
    def __init__(self, db_path):
        self.db_path = db_path
        self._init_db()

    def _init_db(self):
        conn = sqlite3.connect(self.db_path)
        conn.execute(
            "CREATE TABLE IF NOT EXISTS messages (chat_id INTEGER, role TEXT, content TEXT, timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP)")
        conn.execute("CREATE TABLE IF NOT EXISTS whitelist (chat_id INTEGER)")
        conn.close()

    def is_user_in_white_list(self, message: telebot.types.Message):
        chat_id = message.chat.id
        query = "SELECT chat_id FROM whitelist WHERE chat_id = ?"
        conn = sqlite3.connect(self.db_path)
        result = conn.execute(query, (chat_id,)).fetchone()
        conn.close()
        return result is not None

    def add_user_to_whitelist(self, chat_id: int):
        query = "INSERT OR IGNORE INTO whitelist (chat_id) VALUES (?)"
        conn = sqlite3.connect(self.db_path)
        conn.execute(query, (chat_id,))
        conn.commit()
        conn.close()

import os
import sqlite3
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Database connection settings
DATABASE_PATH = os.getenv("DATABASE_PATH", "app.db")

def get_db_connection():
    """Establish a connection to the SQLite database."""
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row  # To return rows as dictionaries
    return conn

def save_uploaded_media(media_id, file_path, media_type):
    """Save metadata of uploaded media to the database."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO uploaded_media (media_id, file_path, media_type)
        VALUES (?, ?, ?)
    """, (media_id, file_path, media_type))
    conn.commit()
    conn.close()

def save_message_log(customer_phone, message_type, content):
    """Save inbound or outbound message logs to the database."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO message_logs (customer_phone, message_type, content, timestamp)
        VALUES (?, ?, ?, datetime('now'))
    """, (customer_phone, message_type, content))
    conn.commit()
    conn.close()
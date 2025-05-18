import os
import mysql.connector # type: ignore
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Database connection settings
DB_CONFIG = {
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
    "host": os.getenv("DB_HOST"),
    "port": os.getenv("DB_PORT"),
    "database": os.getenv("DB_NAME")
}

def get_db_connection():
    """Establish a connection to the MySQL database."""
    conn = mysql.connector.connect(**DB_CONFIG)
    return conn

def save_sender_info(name, phone, email=None):
    """Save sender information to the database."""
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        INSERT IGNORE INTO senders (name, phone, email)
        VALUES (%s, %s, %s)
    """, (name, phone, email))
    conn.commit()
    
    # Get the sender ID
    cursor.execute("SELECT id FROM senders WHERE phone = %s", (phone,))
    sender_id = cursor.fetchone()["id"]
    conn.close()
    return sender_id

def save_message_log(sender_id, customer_phone, message_type, content):
    """Save inbound or outbound message logs to the database."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO message_logs (sender_id, customer_phone, message_type, content, timestamp)
        VALUES (%s, %s, %s, %s, NOW())
    """, (sender_id, customer_phone, message_type, content))
    conn.commit()
    conn.close()
from flask import Flask, request, jsonify
import os
from dotenv import load_dotenv
import mysql.connector
from datetime import datetime

load_dotenv()

app = Flask(__name__)

# Database connection settings
DB_CONFIG = {
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
    "host": os.getenv("DB_HOST"),
    "port": os.getenv("DB_PORT"),
    "database": os.getenv("DB_NAME")
}

def get_db_connection():
    conn = mysql.connector.connect(**DB_CONFIG)
    return conn

def save_customer_contact(phone, name=None, email=None):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        INSERT IGNORE INTO senders (phone, name, email)
        VALUES (%s, %s, %s)
    """, (phone, name, email))
    conn.commit()
    cursor.execute("SELECT id FROM senders WHERE phone = %s", (phone,))
    sender_id = cursor.fetchone()["id"]
    conn.close()
    return sender_id

def log_interaction(sender_id, customer_phone, message_type, content):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO message_logs (sender_id, customer_phone, message_type, content, timestamp)
        VALUES (%s, %s, %s, %s, NOW())
    """, (sender_id, customer_phone, message_type, content))
    conn.commit()
    conn.close()

@app.route('/track-customer', methods=['POST'])
def track_customer():
    data = request.get_json()
    required = ["phone", "message_type", "content"]
    for field in required:
        if field not in data:
            return jsonify({"error": f"{field} is required!"}), 400
    name = data.get("name")
    email = data.get("email")
    phone = data["phone"]
    message_type = data["message_type"]
    content = data["content"]
    sender_id = save_customer_contact(phone, name, email)
    log_interaction(sender_id, phone, message_type, content)
    return jsonify({"message": "Customer and interaction logged successfully!", "sender_id": sender_id}), 200

@app.route('/interactions/<phone>', methods=['GET'])
def get_interactions(phone):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT * FROM message_logs WHERE customer_phone = %s ORDER BY timestamp DESC
    """, (phone,))
    logs = cursor.fetchall()
    conn.close()
    return jsonify(logs)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5050)

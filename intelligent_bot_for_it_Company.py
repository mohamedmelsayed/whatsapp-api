from flask import Flask, request, jsonify
from pywa import WhatsApp, types
import os
from datetime import datetime
from dotenv import load_dotenv
import logging
from functools import wraps

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

flask_app = Flask(__name__)

# Initialize WhatsApp client with error handling
try:
    wa = WhatsApp(
        phone_id=os.getenv("WHATSAPP_PHONE_NUMBER_ID"),
        token=os.getenv("WHATSAPP_ACCESS_TOKEN"),
        server=flask_app,
        verify_token=os.getenv("VERIFY_TOKEN"),
    )
except Exception as e:
    logger.error(f"Failed to initialize WhatsApp client: {str(e)}")
    raise

# Use Redis or database instead of in-memory storage in production
leads = {}

def send_main_menu(user_id: str):
    wa.send_buttons(
        to=user_id,
        header="مرحبا بكم في شركة TechSolutions 💻",
        body="كيف يمكننا مساعدتك اليوم؟",
        buttons=[
            types.Button("خدمات التطوير", "dev_services"),
            types.Button("تهيئة واتساب", "wa_config"),
            types.Button("الحملات التسويقية", "marketing"),
            types.Button("التواصل مع المبيعات", "contact_sales"),
        ]
    )

@wa.on_message
def handle_message(_: WhatsApp, msg: types.Message):
    user_id = msg.from_user.wa_id
    msg.react('👋')
    
    if msg.text.lower() == "menu":
        send_main_menu(user_id)
    else:
        send_main_menu(user_id)
        msg.reply("لقد أرسلت لي رسالة نصية. يرجى استخدام القائمة أدناه:")



@flask_app.route('/')
def home():
    return "TechSolutions WhatsApp Bot is Running!"

if __name__ == '__main__':
    flask_app.run(host='0.0.0.0', port=2626)
from flask import Flask, request, jsonify
from pywa import WhatsApp, types, filters
from pywa.types import CallbackData, Button, CallbackButton
from dataclasses import dataclass
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

@dataclass(frozen=True, slots=True)
class UserData(CallbackData):
    id: int
    name: str
    admin: bool

def send_main_menu(user_id: str):
    wa.send_message(
        to=user_id,
        text="👋 مرحباً بكم في رواسي الإتقان للبرمجيات\nكيف يمكننا مساعدتكم اليوم؟ يرجى اختيار أحد الخيارات التالية:",
        buttons=[
            Button(title="خدمات البرمجيات", callback_data=UserData(id=1, name="dev_services", admin=False)),
            Button(title="الأعمال الذكية", callback_data=UserData(id=2, name="smart_solutions", admin=False)),
            Button(title="استشارات تقنية", callback_data=UserData(id=3, name="consulting", admin=False)),
        ]
    )
   

@wa.on_message
def handle_message(_: WhatsApp, msg: types.Message):
    user_id = msg.from_user.wa_id
    msg.react('🤖')

    text = (msg.text or "").strip().lower()
    if text in ["menu", "القائمة", "ابدأ", "start"]:
        send_main_menu(user_id)
        return
    send_main_menu(user_id)
    msg.reply("يرجى استخدام القائمة أدناه لاختيار الخدمة المطلوبة.")

@wa.on_message(filters.command("start"))
def start(client: WhatsApp, msg: types.Message):
    msg.reply(
        "مرحباً! يرجى إرسال عمرك.",
        buttons=[types.Button("إلغاء", callback_data="cancel")]
    )
    try:
        age = client.listen(
            to=msg.sender,
            filters=filters.message & filters.text,
            cancelers=filters.callback_button & filters.matches("cancel"),
            timeout=20
        )
        msg.reply(f"عمرك هو {age.text}.")
    except listeners.ListenerTimeout:
        msg.reply("لقد استغرقت وقتاً طويلاً لإرسال عمرك.")
    except listeners.ListenerCanceled:
        msg.reply("تم إلغاء العملية.")

@wa.on_callback_button(factory=UserData)
def on_user_data(_: WhatsApp, btn: CallbackButton[UserData]):
    # Example: handle button click using btn.data
    if btn.data.name == "dev_services":
        btn.reply("نقدم خدمات تطوير مواقع وتطبيقات احترافية. لمزيد من التفاصيل أو طلب عرض سعر، أرسل لنا تفاصيل مشروعك.")
    elif btn.data.name == "smart_solutions":
        btn.reply("نقدم حلول الأعمال الذكية مثل الأنظمة المؤسسية والتكامل مع واتساب. تواصل معنا لمناقشة احتياجاتك.")
    elif btn.name == "consulting":
        btn.reply("فريقنا يقدم استشارات تقنية متخصصة في التحول الرقمي وأتمتة الأعمال. احجز استشارتك الآن.")
    else:
        send_main_menu(btn.from_user.wa_id)
        btn.reply("يرجى اختيار خيار من القائمة.")

@flask_app.route('/')
def home():
    return "Rawasy Al-itqan WhatsApp Bot is Running!"

if __name__ == '__main__':
    flask_app.run(host='0.0.0.0', port=2626)
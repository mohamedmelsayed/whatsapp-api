from flask import Flask, request, jsonify
from pywa import WhatsApp, types, filters
from pywa.types import CallbackData, Button, CallbackButton
from dataclasses import dataclass
import os
from datetime import datetime
from dotenv import load_dotenv
import logging
from functools import wraps
import requests

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
   

TRACKING_API_URL = "http://localhost:5050/track-customer"

def log_customer_interaction(phone, message_type, content, name=None, email=None):
    payload = {
        "phone": phone,
        "message_type": message_type,
        "content": content
    }
    if name:
        payload["name"] = name
    if email:
        payload["email"] = email
    try:
        requests.post(TRACKING_API_URL, json=payload, timeout=2)
    except Exception as e:
        logger.warning(f"Failed to log interaction: {e}")

@wa.on_message
def handle_message(_: WhatsApp, msg: types.Message):
    user_id = msg.from_user.wa_id
    msg.react('🤖')
    text = (msg.text or "").strip().lower()
    # Log inbound message
    log_customer_interaction(
        phone=user_id,
        message_type="inbound",
        content=msg.text,
        name=msg.from_user.name if hasattr(msg.from_user, 'name') else None
    )
    if text in ["menu", "القائمة", "ابدأ", "start"]:
        send_main_menu(user_id)
        return
    # Handle service selection by number after dev_services
    if text.isdigit():
        if text == "1":
            reply = "خدمة تكامل واتساب: حلول ربط الأنظمة مع واتساب بزنس، إشعارات تلقائية، بوتات دردشة والمزيد. للمزيد تواصل معنا."
            msg.reply(reply)
            log_customer_interaction(user_id, "outbound", reply)
            return
        elif text == "2":
            reply = "قائمة QR للمطاعم: تصميم قوائم رقمية تفاعلية لعرضها عبر رمز QR لعملائك. اطلب عرضك الآن."
            msg.reply(reply)
            log_customer_interaction(user_id, "outbound", reply)
            return
        elif text == "3":
            reply = "خدمات الأتمتة والجدولة: أتمتة العمليات وجدولة المهام لتوفير الوقت وزيادة الإنتاجية. تواصل لمناقشة احتياجاتك."
            msg.reply(reply)
            log_customer_interaction(user_id, "outbound", reply)
            return
        elif text == "4":
            reply = "تطبيقات مخصصة: تطوير تطبيقات وبرمجيات حسب متطلباتك الخاصة. أرسل لنا فكرتك لنبدأ التنفيذ."
            msg.reply(reply)
            log_customer_interaction(user_id, "outbound", reply)
            return
        elif text == "0":
            send_main_menu(user_id)
            reply = "تمت إعادتك للقائمة الرئيسية."
            msg.reply(reply)
            log_customer_interaction(user_id, "outbound", reply)
            return
    send_main_menu(user_id)
    reply = "يرجى استخدام القائمة أدناه لاختيار الخدمة المطلوبة أو كتابة رقم الخدمة."
    msg.reply(reply)
    log_customer_interaction(user_id, "outbound", reply)

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
    # Log button click as inbound
    log_customer_interaction(
        phone=btn.from_user.wa_id,
        message_type="inbound",
        content=f"Button: {btn.data.name}",
        name=btn.from_user.name if hasattr(btn.from_user, 'name') else None
    )
    if btn.data.name == "dev_services":
        text = "خدماتنا البرمجية:\n1. تكامل واتساب\n2. قائمة QR للمطاعم\n3. الأتمتة وخدمات الجدولة\n4. تطبيقات مخصصة\n\nيرجى كتابة رقم الخدمة المطلوبة أو أرسل 0 للعودة للقائمة الرئيسية."
        btn.message.reply(text)
        log_customer_interaction(btn.from_user.wa_id, "outbound", text)
    elif btn.data.name == "wa_integration":
        text = "خدمة تكامل واتساب: حلول ربط الأنظمة مع واتساب بزنس، إشعارات تلقائية، بوتات دردشة والمزيد. للمزيد تواصل معنا."
        btn.message.reply(text)
        log_customer_interaction(btn.from_user.wa_id, "outbound", text)
    elif btn.data.name == "qr_menu":
        text = "قائمة QR للمطاعم: تصميم قوائم رقمية تفاعلية لعرضها عبر رمز QR لعملائك. اطلب عرضك الآن."
        btn.message.reply(text)
        log_customer_interaction(btn.from_user.wa_id, "outbound", text)
    elif btn.data.name == "automation":
        text = "خدمات الأتمتة والجدولة: أتمتة العمليات وجدولة المهام لتوفير الوقت وزيادة الإنتاجية. تواصل لمناقشة احتياجاتك."
        btn.message.reply(text)
        log_customer_interaction(btn.from_user.wa_id, "outbound", text)
    elif btn.data.name == "custom_apps":
        text = "تطبيقات مخصصة: تطوير تطبيقات وبرمجيات حسب متطلباتك الخاصة. أرسل لنا فكرتك لنبدأ التنفيذ."
        btn.message.reply(text)
        log_customer_interaction(btn.from_user.wa_id, "outbound", text)
    elif btn.data.name == "main_menu":
        send_main_menu(btn.from_user.wa_id)
        text = "تمت إعادتك للقائمة الرئيسية."
        btn.message.reply(text)
        log_customer_interaction(btn.from_user.wa_id, "outbound", text)
    elif btn.data.name == "smart_solutions":
        text = "نقدم حلول الأعمال الذكية مثل الأنظمة المؤسسية والتكامل مع واتساب. تواصل معنا لمناقشة احتياجاتك."
        btn.message.reply(text)
        log_customer_interaction(btn.from_user.wa_id, "outbound", text)
    elif btn.data.name == "consulting":
        text = "فريقنا يقدم استشارات تقنية متخصصة في التحول الرقمي وأتمتة الأعمال. احجز استشارتك الآن."
        btn.message.reply(text)
        log_customer_interaction(btn.from_user.wa_id, "outbound", text)
    else:
        send_main_menu(btn.from_user.wa_id)
        text = "يرجى اختيار خيار من القائمة."
        btn.message.reply(text)
        log_customer_interaction(btn.from_user.wa_id, "outbound", text)

@flask_app.route('/')
def home():
    return "Rawasy Al-itqan WhatsApp Bot is Running!"

if __name__ == '__main__':
    flask_app.run(host='0.0.0.0', port=2626)
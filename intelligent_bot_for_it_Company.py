from flask import Flask
from pywa import WhatsApp, types
import os
from datetime import datetime

flask_app = Flask(__name__)

wa = WhatsApp(
    phone_id=os.getenv("WHATSAPP_PHONE_NUMBER_ID"),
    token=os.getenv("WHATSAPP_ACCESS_TOKEN"),
    server=flask_app,
    verify_token=os.getenv("VERIFY_TOKEN"),
)

# Temporary storage for leads (use database in production)
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

@wa.on_button_click("dev_services")
def dev_services(_: WhatsApp, clk: types.ButtonClick):
    clk.reply(
        header="🚀 خدمات التطوير لدينا",
        body="""نقدم حلول برمجية متكاملة:
- تطبيقات ويب/موبايل
- أنظمة إدارة الشركات
- تكاملات API
- حلول الذكاء الاصطناعي""",
        buttons=[
            types.Button("عرض أسعار", "dev_pricing"),
            types.Button("حجز استشارة", "book_meeting"),
            types.Button("العودة للقائمة", "main_menu")
        ]
    )

@wa.on_button_click("wa_config")
def wa_config(_: WhatsApp, clk: types.ButtonClick):
    clk.reply(
        header="📱 تهيئة واتساب بزنس",
        body="""خدماتنا تشمل:
- إعداد API متكامل
- بناء روبوت محادثة ذكي
- تكامل مع CRM
- حلول إرسال جماعي معتمدة""",
        buttons=[
            types.Button("الأسعار", "wa_pricing"),
            types.Button("طلب الخدمة", "order_service"),
            types.Button("نماذج أعمال", "portfolio")
        ]
    )

@wa.on_button_click("marketing")
def marketing(_: WhatsApp, clk: types.ButtonClick):
    clk.reply_document(
        document="https://example.com/marketing-proposal.pdf",
        filename="marketing-proposal.pdf",
        caption="📈 نموذج لحملة تسويقية ناجحة"
    )
    clk.reply(
        body="لطلب حملة مخصصة، اختر أحد الخيارات:",
        buttons=[
            types.Button("حملة رسائل", "msg_campaign"),
            types.Button("حملة بروشور", "brochure_campaign"),
            types.Button("اتصل بنا", "contact_sales")
        ]
    )

@wa.on_button_click("contact_sales")
def contact_sales(_: WhatsApp, clk: types.ButtonClick):
    leads[clk.from_user.wa_id] = {"stage": "contact"}
    clk.reply(
        body="يرجى إرسال معلومات التواصل:",
        buttons=[
            types.QuickReply("البريد الإلكتروني 📧", "email"),
            types.QuickReply("رقم الهاتف 📞", "phone")
        ]
    )

@wa.on_quick_reply("email")
def handle_email(_: WhatsApp, qr: types.QuickReply):
    user_id = qr.from_user.wa_id
    leads[user_id]["contact_type"] = "email"
    qr.reply("أرسل عنوان بريدك الإلكتروني وسنتواصل معك خلال ٢٤ ساعة")

@wa.on_quick_reply("phone")
def handle_phone(_: WhatsApp, qr: types.QuickReply):
    user_id = qr.from_user.wa_id
    leads[user_id]["contact_type"] = "phone"
    qr.reply("أرسل رقم هاتفك وسنتواصل معك خلال ٢٤ ساعة")

@wa.on_message
def handle_contact_info(_: WhatsApp, msg: types.Message):
    user_id = msg.from_user.wa_id
    if user_id in leads and leads[user_id].get("stage") == "contact":
        contact_type = leads[user_id]["contact_type"]
        leads[user_id]["info"] = msg.text
        leads[user_id]["timestamp"] = datetime.now().isoformat()
        
        msg.reply(f"تم استلام {contact_type} بنجاح ✅\nسنقوم بالتواصل معك قريبًا!")
        send_main_menu(user_id)
        del leads[user_id]

@wa.on_button_click("main_menu")
def return_to_menu(_: WhatsApp, clk: types.ButtonClick):
    send_main_menu(clk.from_user.wa_id)

@flask_app.route('/')
def home():
    return "TechSolutions WhatsApp Bot is Running!"

if __name__ == '__main__':
    flask_app.run(host='0.0.0.0', port=2626)

# ==========================

from flask import Flask
from pywa import WhatsApp, types
import os


# Initialize Flask app first
flask_app = Flask(__name__)

# Initialize WhatsApp AFTER Flask app
wa = WhatsApp(
    phone_id=os.getenv("WHATSAPP_PHONE_NUMBER_ID"),
    token=os.getenv("WHATSAPP_ACCESS_TOKEN"),
    server=flask_app,
    verify_token='11335577664422',
)

# Use the correct decorator (flask_app.route instead of app.route)
@flask_app.route('/')
def home():
    return "Flask is running on port 2626!"

@wa.on_message
def hello(_: WhatsApp, msg: types.Message):
    msg.react('👋')
    msg.reply(f'Hello {msg.from_user.name} we are here to serve! you  here is a sample how to attach a pdf file *this api configuration will cost you only $$$*!')
    send_doc(
        user_id=msg.from_user.wa_id,
        document='https://drive.google.com/file/d/1J15-YMivJp5docLMmyGL_q8kLUFd3_BP/view?usp=sharing',
        filename='example.pdf',
        type='pdf',
        caption='Example PDF'
    )

def send_doc( user_id: str, document: str, filename: str, caption: str):
    wa.send_document(
     mime_type='application/pdf',
        to=user_id,
        document=document,
        filename=filename,
        caption=caption
    )

if __name__ == '__main__':
    # Remove the duplicate flask_app.run() at the bottom
    flask_app.run(host='0.0.0.0', port=2626)
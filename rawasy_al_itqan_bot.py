from flask import Flask, request, jsonify
from pywa import WhatsApp, types
from pywa.types import NewTemplate as NewTemp
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Initialize WhatsApp client
wa = WhatsApp(
    phone_id=os.getenv("WHATSAPP_PHONE_NUMBER_ID"),
    token=os.getenv("WHATSAPP_ACCESS_TOKEN"),
    server=app,
    verify_token=os.getenv("VERIFY_TOKEN"),
    app_id=os.getenv("APP_ID"),
)

def send_services_menu(user_id: str):
    
    wa.create_template(

        template=NewTemp(

            name='buy_new_iphone_x',

            category=NewTemp.Category.MARKETING,

            language=NewTemp.Language.ENGLISH_US,

            header=NewTemp.Text('The New iPhone {15} is here!'),

            body=NewTemp.Body('Buy now and use the code {WA_IPHONE_15} to get {15%} off!'),

            footer=NewTemp.Footer('Powered by PyWa'),

            buttons=[

                NewTemp.UrlButton(title='Buy Now', url='https://example.com/shop/{iphone15}'),

                NewTemp.PhoneNumberButton(title='Call Us', phone_number='1234567890'),

                NewTemp.QuickReplyButton('Unsubscribe from marketing messages'),

                NewTemp.QuickReplyButton('Unsubscribe from all messages'),

            ],

        ),

)

@wa.on_message
def handle_message(_: WhatsApp, msg: types.Message):
    user_id = msg.from_user.wa_id
    msg.react('👋')

    if msg.text.lower() in ["menu", "قائمة"]:
        send_services_menu(user_id)
     

        msg.reply("Please use the menu below to navigate our services.")
    else:
        send_services_menu(user_id)
        msg.reply("Please use the menu below to navigate our services.")

@app.route('/')
def home():
    return "Rawasy Al-Itqan WhatsApp Bot is Running!"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=2626)
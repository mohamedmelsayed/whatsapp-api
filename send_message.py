from venv import logger
from pywa import WhatsApp
from flask import Flask, request, jsonify
from dotenv import load_dotenv
import os
load_dotenv()
import requests


app = Flask(__name__)

# Initialize WhatsApp client
WHATSAPP_PHONE_NUMBER_ID= os.getenv("WHATSAPP_PHONE_NUMBER_ID") 
WHATSAPP_ACCESS_TOKEN= os.getenv("WHATSAPP_ACCESS_TOKEN")
wa = WhatsApp(
    phone_id=os.getenv("WHATSAPP_PHONE_NUMBER_ID"),
    token=os.getenv("WHATSAPP_ACCESS_TOKEN"),
    business_account_id=os.getenv("WHATSAPP_WABA_ID"),
  
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



@app.route('/send_message', methods=['POST'])
def send_message():
    data = request.json
    to = data.get('to')
    text = data.get('text')
    try:
        response = wa.send_message(to=to, text=text)
        log_customer_interaction(to, "outbound", text)

        return jsonify({'status': 'success', 'response': response}), 200
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 400

@app.route('/send_template_message', methods=['POST'])
def send_template_message():
    data = request.json
    to = data.get('to')
    template_name = data.get('template_name')
    language = data.get('language', 'en_US')
    parameters = data.get('parameters', [])
    access_token = os.getenv('WHATSAPP_ACCESS_TOKEN')
    phone_number_id = os.getenv('WHATSAPP_PHONE_NUMBER_ID')
    url = f"https://graph.facebook.com/v18.0/{phone_number_id}/messages"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    # Build the template payload for Graph API
    payload = {
        "messaging_product": "whatsapp",
        "to": to,
        "type": "template",
        "template": {
            "name": template_name,
            "language": {"code": language},
            "components": [
                {
                    "type": "body",
                    "parameters": [
                        {"type": "text", "text": str(param)} for param in parameters
                    ]
                }
            ] if parameters else []
        }
    }
    try:
        response = requests.post(url, headers=headers, json=payload)
        log_customer_interaction(to, "outbound", template_name)

        return jsonify({'status': 'success', 'response': response.json()}), response.status_code
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 400


# --- واجهة REST لاستقبال البيانات ---
@app.route('/send-invoice', methods=['POST'])
def handle_invoice():
    try:
        customer_phone = request.form.get('customer_phone')
        name = request.form.get('name')
        invoice_number = request.form.get('invoice_number')
        amount = request.form.get('amount')
        currency = request.form.get('currency')
        file = request.files.get('file')

        # التحقق من البيانات المطلوبة
        if not all([customer_phone, name, invoice_number, amount, currency, file]):
            return jsonify({"error": "جميع الحقول مطلوبة بما في ذلك الملف."}), 400

        # رفع الملف
        media_id = upload_document(file)

        # إرسال الرسالة
        result = send_document(
            media_id=media_id,
            customer_phone=customer_phone,
            name=name,
            invoice_number=invoice_number,
            amount=amount,
            currency=currency
        )

        return jsonify({"message": "تم إرسال الفاتورة بنجاح!", "media_id": media_id, "response": result}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
     
# --- 1. رفع الملف إلى ميتا ---
def upload_document(file):
    url = f"https://graph.facebook.com/v18.0/{WHATSAPP_PHONE_NUMBER_ID}/media"

    headers = {
        "Authorization": f"Bearer {WHATSAPP_ACCESS_TOKEN}"
    }

    payload = {
        "messaging_product": "whatsapp",
        "type": "document"
    }

    files = {"file": (file.filename, file.stream, file.content_type)}

    response = requests.post(url, headers=headers, data=payload, files=files)

    if response.status_code != 200:
        raise Exception(f"فشل رفع الملف: {response.text}")

    return response.json().get("id")  # Media ID


# --- 2. إرسال الرسالة مع Media ID والمتغيرات ---
def send_document(media_id, customer_phone, name, invoice_number, amount, currency):
    url = f"https://graph.facebook.com/v18.0/{WHATSAPP_PHONE_NUMBER_ID}/messages"
    
    headers = {
        "Authorization": f"Bearer {WHATSAPP_ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }
    
    data = {
        "messaging_product": "whatsapp",
        "to": customer_phone,
        "type": "document",
        "document": {
            "id": media_id,
            "filename": "invoice.pdf",
            "caption": f"""عزيزنا العميل {name},
مرفق تفاصيل طلبكم الأخير بالرقم {invoice_number} بمبلغ {amount} {currency}.
شكرًا لتعاملكم معنا."""
        }
    }
    
    response = requests.post(url, headers=headers, json=data)
    log_customer_interaction(customer_phone, "outbound", f"sending {media_id} for invoice {invoice_number} pdf")

    return response.json()



if __name__ == '__main__':
       app.run(host='0.0.0.0', port=8888)



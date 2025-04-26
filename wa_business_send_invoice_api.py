import requests
import os
from flask import Flask, request, jsonify

app = Flask(__name__)

# --- إعدادات واتساب ---
WHATSAPP_ACCESS_TOKEN = os.getenv("WHATSAPP_ACCESS_TOKEN")
WHATSAPP_PHONE_NUMBER_ID = os.getenv("WHATSAPP_PHONE_NUMBER_ID")

# --- 1. رفع الملف إلى ميتا ---
def upload_document(file_path):
    url = f"https://graph.facebook.com/v18.0/{WHATSAPP_PHONE_NUMBER_ID}/media"
    
    headers = {
        "Authorization": f"Bearer {WHATSAPP_ACCESS_TOKEN}"
    }
    
    payload = {
        "messaging_product": "whatsapp",
        "type": "document"
    }
    
    # تأكد أن الملف موجود وصيغته PDF
    if not os.path.exists(file_path):
        raise Exception("الملف غير موجود!")
    
    with open(file_path, "rb") as file:
        files = {"file": (os.path.basename(file_path), file, "application/pdf")}
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
    return response.json()

# --- واجهة REST لاستقبال البيانات ---
@app.route('/send-invoice', methods=['POST'])
def handle_invoice():
    try:
        data = request.get_json()
        
        # التحقق من البيانات المطلوبة
        required_fields = ['customer_phone', 'name', 'invoice_number', 'amount', 'currency', 'file_path']
        for field in required_fields:
            if field not in data:
                return jsonify({"error": f"المتغير {field} مطلوب!"}), 400
        
        # رفع الملف
        media_id = upload_document(data['file_path'])
        
        # إرسال الرسالة
        result = send_document(
            media_id=media_id,
            customer_phone=data['customer_phone'],
            name=data['name'],
            invoice_number=data['invoice_number'],
            amount=data['amount'],
            currency=data['currency']
        )
        
        return jsonify({"message": "تم الإرسال!", "media_id": media_id, "response": result}), 200
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)



#     curl -X POST http://localhost:5000/send-invoice \
# -H "Content-Type: application/json" \
# -d '{
#      "customer_phone": "249122302757",
#      "name": "أحمد محمد",
#      "invoice_number": "INV-2023-456",
#      "amount": "750",
#      "currency": "SAR",
#      "file_path": "/home/mr-mohamed/Downloads/pdf/aktshf-mtah-altalm.pdf"
# }'


# عزيزنا العميل {{1}}،
# مرفق تفاصيل طلبكم الأخير بالرقم {{2}} بمبلغ {{3}} {{4}}.
# شكرًا لتعاملكم معنا.
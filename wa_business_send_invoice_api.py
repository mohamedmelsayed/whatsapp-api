from dotenv import load_dotenv
import requests
import os
from flask import Flask, request, jsonify
load_dotenv()

app = Flask(__name__)

# --- إعدادات واتساب ---
WHATSAPP_ACCESS_TOKEN = os.getenv("WHATSAPP_ACCESS_TOKEN")
WHATSAPP_PHONE_NUMBER_ID = os.getenv("WHATSAPP_PHONE_NUMBER_ID")

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
    return response.json()

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
    


# Add these new functions after the existing code, before if __name__ == '__main__':

def upload_video(file_path):
    """Upload video file to Meta servers"""
    url = f"https://graph.facebook.com/v18.0/{WHATSAPP_PHONE_NUMBER_ID}/media"
    
    headers = {
        "Authorization": f"Bearer {WHATSAPP_ACCESS_TOKEN}"
    }
    
    payload = {
        "messaging_product": "whatsapp",
        "type": "video"
    }
    
    if not os.path.exists(file_path):
        raise Exception("Video file not found!")
    
    with open(file_path, "rb") as file:
        files = {"file": (os.path.basename(file_path), file, "video/mp4")}
        response = requests.post(url, headers=headers, data=payload, files=files)
    
    if response.status_code != 200:
        raise Exception(f"Failed to upload video: {response.text}")
    
    return response.json().get("id")

@app.route('/send-promotion', methods=['POST'])
def handle_promotion():
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['customer_phone', 'video_path', 'promo_text', 'button_text', 'button_url']
        for field in required_fields:
            if field not in data:
                return jsonify({"error": f"Field {field} is required!"}), 400
        
        # Upload video
        video_id = upload_video(data['video_path'])
        
        # Send promotional message
        result = send_promotion(
            video_id=video_id,
            customer_phone=data['customer_phone'],
            promo_text=data['promo_text'],
            button_text=data['button_text'],
            button_url=data['button_url']
        )
        
        return jsonify({
            "message": "Promotion sent successfully!", 
            "video_id": video_id, 
            "response": result
        }), 200
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    

def send_promotion_with_url(customer_phone, video_url, promo_text, button_text, button_url):
    """Send promotional message with video URL and CTA button"""
    url = f"https://graph.facebook.com/v18.0/{WHATSAPP_PHONE_NUMBER_ID}/messages"
    
    headers = {
        "Authorization": f"Bearer {WHATSAPP_ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }
    
    data = {
        "messaging_product": "whatsapp",
        "to": customer_phone,
        "type": "video",
        "video": {
            "link": video_url,
            "caption": promo_text
        }
    }
    
    response = requests.post(url, headers=headers, json=data)
    return response.json()

@app.route('/send-promotion-url', methods=['POST'])
def handle_promotion_url():
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['customer_phone', 'video_url', 'promo_text', 'button_text', 'button_url']
        for field in required_fields:
            if field not in data:
                return jsonify({"error": f"Field {field} is required!"}), 400
        
        # Send promotional message
        result = send_promotion_with_url(
            customer_phone=data['customer_phone'],
            video_url=data['video_url'],
            promo_text=data['promo_text'],
            button_text=data['button_text'],
            button_url=data['button_url']
        )
        
        return jsonify({
            "message": "Promotion sent successfully!", 
            "response": result
        }), 200
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    

def send_promotion(video_id, customer_phone, promo_text, button_text, button_url):
    """Send promotional message with video and CTA button"""
    url = f"https://graph.facebook.com/v18.0/{WHATSAPP_PHONE_NUMBER_ID}/messages"
    
    headers = {
        "Authorization": f"Bearer {WHATSAPP_ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }
    # customer_phone="96895259944";
    
    # First send the video message
    video_message = {
        "messaging_product": "whatsapp",
        "to": customer_phone,
        "type": "video",
        "video": {
            "id": video_id,
            "caption": promo_text
        }
    }
    
    # Send video first
    video_response = requests.post(url, headers=headers, json=video_message)
    
    # Then send the interactive button message
    button_message = {
        "messaging_product": "whatsapp",
        "to": customer_phone,
        "type": "interactive",
        "interactive": {
            "type": "button",
            "body": {
                "text": "Click below to learn more!"
            },
            "action": {
                "buttons": [
                    {
                        "type": "reply",
                        "button": button_text,  # Changed from "title" to "text"
                        "url": button_url
                    }
                ]
            }
        }
    }
    
    # Send button message
    button_response = requests.post(url, headers=headers, json=button_message)
    
    return {
        "video_response": video_response.json(),
        "button_response": button_response.json()
    }

if __name__ == '__main__':
    app.run(debug=True, port=8888)


# curl -X POST SERVER_URL/send-invoice \
# -H "Content-Type: multipart/form-data" \
# -F "customer_phone=966504677306" \
# -F "name=أحمد محمد" \
# -F "invoice_number=INV-2023-456" \
# -F "amount=750" \
# -F "currency=SAR" \
# -F "file=@/home/mr-mohamed/Downloads/pdf/aktshf-mtah-altalm.pdf"

#     curl -X POST SERVER_URL/send-invoice \
# -H "Content-Type: application/json" \
# -d '{
#      "customer_phone": "96898157645",
#      "name": "أحمد محمد",
#      "invoice_number": "INV-2023-456",
#      "amount": "750",
#      "currency": "SAR",
#      "file_path": "/home/mr-mohamed/Downloads/pdf/aktshf-mtah-altalm.pdf"
# }'


# curl -X POST http://localhost:5000/send-promotion-url \
# -H "Content-Type: application/json" \
# -d '{
#     "customer_phone": "249122302757",
#     "video_url": "https://www.youtube.com/watch?v=HdEzeiSR5eU",
#     "promo_text": "Check out our latest promotion!",
#     "button_text": "Shop Now",
#     "button_url": "https://rawasy-al-itqan.prof-dev.com"
# }'

# عزيزنا العميل {{1}}،
# مرفق تفاصيل طلبكم الأخير بالرقم {{2}} بمبلغ {{3}} {{4}}.
# شكرًا لتعاملكم معنا.


# curl -X POST http://localhost:5000/send-promotion \
# -H "Content-Type: application/json" \
# -d '{
#     "customer_phone": "249122302757",
#     "video_path": "/media/mr-mohamed/Crucial X6/Yt Content/odoo tricks.mp4",
#     "promo_text": "Check out our amazing summer sale! 🌞",
#     "button_text": "Shop Now",
#     "button_url": "https://rawasy-al-itqan.prof-dev.com"
# }'



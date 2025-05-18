from dotenv import load_dotenv
import os
import requests
from flask import Flask, request, jsonify
from utils import save_sender_info, save_message_log
from whatsapp import upload_document, send_document
load_dotenv()

WHATSAPP_ACCESS_TOKEN = os.getenv("WHATSAPP_ACCESS_TOKEN")
WHATSAPP_PHONE_NUMBER_ID = os.getenv("WHATSAPP_PHONE_NUMBER_ID")

app = Flask(__name__)

@app.route('/send-invoice', methods=['POST'])
def handle_invoice():
    try:
        data = request.get_json()
        required_fields = ['sender_name', 'sender_phone', 'sender_email', 'customer_phone', 'name', 'invoice_number', 'amount', 'currency', 'file_path']
        for field in required_fields:
            if field not in data:
                return jsonify({"error": f"{field} is required!"}), 400
        
        # Save sender information
        # sender_id = save_sender_info(
        #     name=data['sender_name'],
        #     phone=data['sender_phone'],
        #     email=data.get('sender_email')
        # )
        
        # Upload the document
        media_id = upload_document(data['file_path'])
        
        # Send the document
        result = send_document(
            media_id=media_id,
            customer_phone=data['customer_phone'],
            name=data['name'],
            invoice_number=data['invoice_number'],
            amount=data['amount'],
            currency=data['currency']
        )
        
        # Log the message
        save_message_log(
            sender_id=sender_id,
            customer_phone=data['customer_phone'],
            message_type="outbound",
            content=f"Invoice sent for {data['amount']} {data['currency']}"
        )
        
        return jsonify({"message": "Invoice sent successfully!", "media_id": media_id, "response": result}), 200
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
    customer_phone="96895259944";
    
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
    # video_response = requests.post(url, headers=headers, json=video_message)
    
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
    app.run(debug=True)
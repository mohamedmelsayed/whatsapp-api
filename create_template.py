from flask import Flask, request, jsonify
import requests
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

# Facebook Graph API credentials (store in .env)
ACCESS_TOKEN = os.getenv('WHATSAPP_ACCESS_TOKEN')
PHONE_NUMBER_ID = os.getenv('WHATSAPP_PHONE_NUMBER_ID')
API_VERSION = 'v18.0'  # Update to latest version

@app.route('/send-promotion', methods=['POST'])
def send_promotion():
    try:
        data = request.json
        to_number = data['to_number']  # Include country code (e.g., 14151234567)
        template_name = data['template_name']
        parameters = data['parameters']  # e.g., ["50% off", "https://example.com"]

        # Send message via Facebook Graph API
        url = f'https://graph.facebook.com/{API_VERSION}/{PHONE_NUMBER_ID}/messages'
        headers = {
            'Authorization': f'Bearer {ACCESS_TOKEN}',
            'Content-Type': 'application/json'
        }
        payload = {
            "messaging_product": "whatsapp",
            "to": to_number,
            "type": "template",
            "template": {
                "name": template_name,
                "language": {
                    "code": "en"  # Use appropriate language code
                },
                "components": [
                    {
                        "type": "body",
                        "parameters": [
                            {"type": "text", "text": parameters[0]},  # Dynamic text
                        ]
                    }
                ]
            }
        }

        response = requests.post(url, headers=headers, json=payload)
        response_data = response.json()

        if response.status_code == 200:
            return jsonify({"status": "success", "message_id": response_data.get('messages')[0]['id']}), 200
        else:
            return jsonify({"status": "error", "details": response_data}), 400

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
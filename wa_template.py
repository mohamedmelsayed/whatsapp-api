from venv import logger
from pywa import WhatsApp
from flask import Flask, request, jsonify
from dotenv import load_dotenv
import os
load_dotenv()


app = Flask(__name__)

# Initialize WhatsApp client

wa = WhatsApp(
    phone_id=os.getenv("WHATSAPP_PHONE_NUMBER_ID"),
    token=os.getenv("WHATSAPP_ACCESS_TOKEN"),
    business_account_id=os.getenv("WHATSAPP_WABA_ID"),
  
)   


from pywa.types import NewTemplate as NewTemp

@app.route('/create_template', methods=['POST'])
def create_template():
    data = request.json
    try:
        template_kwargs = {
            "name": data['name'],
            "category": getattr(NewTemp.Category, data.get('category', 'MARKETING').upper()),
            "language": getattr(NewTemp.Language, data.get('language', 'ENGLISH_US').upper().replace('EN_US', 'ENGLISH_US'))
        }
        if data.get('header'):
            template_kwargs["header"] = NewTemp.Text(data['header'])
        if data.get('body'):
            template_kwargs["body"] = NewTemp.Body(data['body'])
        if data.get('footer'):
            template_kwargs["footer"] = NewTemp.Footer(data['footer'])
        if data.get('buttons'):
            template_kwargs["buttons"] = [
                NewTemp.UrlButton(title=btn['title'], url=btn['url']) if btn['type'] == 'url' else
                NewTemp.PhoneNumberButton(title=btn['title'], phone_number=btn['phone_number']) if btn['type'] == 'phone' else
                NewTemp.QuickReplyButton(btn['title'])
                for btn in data['buttons']
            ]
        template = NewTemp(**template_kwargs)
        response = wa.create_template(template=template)
        return jsonify({'status': 'success', 'response': response}), 201
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 400

@app.route('/create_template_graph', methods=['POST'])
def create_template_graph():
    data = request.json
    name = data.get('name')
    language = data.get('language', 'en_US')
    category = data.get('category', 'TRANSACTIONAL')
    components = data.get('components', [])
    try:
        result = create_template_facebook_graphql(name, language, category, components)
        return jsonify({'status': 'success', 'response': result}), 201
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 400

import requests

def create_template_facebook_graphql(name, language, category, components):
    """
    Create a WhatsApp message template using Facebook Graph API v22 (without pywa).
    """
    import os
    from dotenv import load_dotenv
    load_dotenv()
    access_token = os.getenv('WHATSAPP_ACCESS_TOKEN')
    phone_number_id = os.getenv('WHATSAPP_PHONE_NUMBER_ID')
    url = f"https://graph.facebook.com/v22.0/{phone_number_id}/message_templates"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    payload = {
        "name": name,
        "language": language,
        "category": category,
        "components": components
    }
    response = requests.post(url, headers=headers, json=payload)
    return response.json()

@app.route('/send_message', methods=['POST'])
def send_message():
    data = request.json
    to = data.get('to')
    text = data.get('text')
    try:
        response = wa.send_message(to=to, text=text)
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
        return jsonify({'status': 'success', 'response': response.json()}), response.status_code
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True)


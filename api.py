import os
from dotenv import load_dotenv
import requests
import json
from typing import Dict, Any
# Load environment variables
load_dotenv()

class WhatsAppTemplateAPI:
    def __init__(self, access_token: str, phone_number_id: str):
        self.access_token = access_token
        self.phone_number_id = phone_number_id
        self.api_url = f"https://graph.facebook.com/v22.0/{phone_number_id}/messages"
        self.headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json"
        }

    def send_template_message(
        self, 
        to_phone: str, 
        template_name: str, 
        language_code: str = "en",
        components: Dict[str, Any] = None
    ) -> Dict:
        """
        Send a template message to a WhatsApp number
        
        Args:
            to_phone: Recipient's phone number
            template_name: Name of the approved template
            language_code: Template language code
            components: Template components (header, body, buttons)
        """
        payload = {
            "messaging_product": "whatsapp",
            "to": to_phone,
            "template": {
                "name": template_name,
                "language": {
                    "code": language_code
                }
            }
        }

        if components:
            payload["template"]["components"] = components

        response = requests.post(
            self.api_url,
            headers=self.headers,
            json=payload
        )
        
        return response.json()
    



phone_number_id=os.getenv("WHATSAPP_PHONE_NUMBER_ID"),
access_token=os.getenv("WHATSAPP_ACCESS_TOKEN")
api = WhatsAppTemplateAPI(access_token, phone_number_id)

# Example template components
components = {
    "body": {
        "parameters": [
            {
                "type": "text",
                "text": "John Doe"
            },
            {
                "type": "text",
                "text": "123456"
            }
        ]
    }
}

# Send template message
response = api.send_template_message(
    to_phone="96898157645",
    template_name="sample_template",
    language_code="en",
    components=components
)

print(json.dumps(response, indent=2))
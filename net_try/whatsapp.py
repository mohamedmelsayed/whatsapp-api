import os
import requests

WHATSAPP_ACCESS_TOKEN = os.getenv("WHATSAPP_ACCESS_TOKEN")
WHATSAPP_PHONE_NUMBER_ID = os.getenv("WHATSAPP_PHONE_NUMBER_ID")

def upload_document(file_path):
    """Upload a document to WhatsApp servers."""
    url = f"https://graph.facebook.com/v18.0/{WHATSAPP_PHONE_NUMBER_ID}/media"
    headers = {
        "Authorization": f"Bearer {WHATSAPP_ACCESS_TOKEN}"
    }
    payload = {
        "messaging_product": "whatsapp",
        "type": "document"
    }
    if not os.path.exists(file_path):
        raise Exception("File not found!")
    with open(file_path, "rb") as file:
        files = {"file": (os.path.basename(file_path), file, "application/pdf")}
        response = requests.post(url, headers=headers, data=payload, files=files)
    if response.status_code != 200:
        raise Exception(f"Failed to upload file: {response.text}")
    return response.json().get("id")

def send_document(media_id, customer_phone, name, invoice_number, amount, currency):
    """Send a document via WhatsApp."""
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
            "caption": f"""Dear {name},
Attached are the details of your recent order #{invoice_number} for {amount} {currency}.
Thank you for doing business with us."""
        }
    }
    response = requests.post(url, headers=headers, json=data)
    if response.status_code != 200:
        raise Exception(f"Failed to send document: {response.text}")
    return response.json()
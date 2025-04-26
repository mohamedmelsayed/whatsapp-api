import requests
import json
import os

# --- الإعدادات الأساسية ---
ACCESS_TOKEN =  os.getenv("WHATSAPP_ACCESS_TOKEN")
PHONE_NUMBER_ID =os.getenv("WHATSAPP_PHONE_NUMBER_ID") # استبدله بـ WhatsApp Business Account ID
RECIPIENT_NUMBER = "966504677306"  # رقم العميل (بالتنسيق الدولي: 201234567890)
FILE_PATH = "/home/mr-mohamed/Downloads/pdf/aktshf-mtah-altalm.pdf"  # مسار الملف المراد رفعه

# --- 1. رفع الملف إلى سيرفرات فيسبوك ---
def upload_media(file_path):
    url = f"https://graph.facebook.com/v18.0/{PHONE_NUMBER_ID}/media"
    
    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}"
    }
    
    payload = {
        "messaging_product": "whatsapp",
        "type": "document"
    }
    
    files = {
        "file": (os.path.basename(file_path), open(file_path, "rb"), "application/pdf")
    }
    
    response = requests.post(url, headers=headers, data=payload, files=files)
    
    if response.status_code == 200:
        return response.json().get("id")  # يُعيد Media ID
    else:
        raise Exception(f"فشل الرفع: {response.text}")

# --- 2. إرسال الملف إلى العميل ---
def send_document(media_id, recipient_number):
    url = f"https://graph.facebook.com/v18.0/{PHONE_NUMBER_ID}/messages"
    
    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }
    
    data = {
        "messaging_product": "whatsapp",
        "recipient_type": "individual",
        "to": recipient_number,
        "type": "document",
        "document": {
            "id": media_id,
            "filename": "اختبار باييثون.pdf",  # يمكنك تغيير اسم الملف
            "caption": " مرفوع بكود بايثون تفضل الملف المطلوب 📄"  # نص توضيحي (اختياري)
        }
    }
    
    response = requests.post(url, headers=headers, json=data)
    
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"فشل الإرسال: {response.text}")

# --- التشغيل الرئيسي ---
if __name__ == "__main__":
    try:
        # 1. رفع الملف
        media_id = upload_media(FILE_PATH)
        print(f"تم الرفع بنجاح! Media ID: {media_id}")
        
        # 2. إرسال الملف
        response = send_document(media_id, RECIPIENT_NUMBER)
        print("تم الإرسال بنجاح:", json.dumps(response, indent=2))
        
    except Exception as e:
        print("حدث خطأ:", str(e))
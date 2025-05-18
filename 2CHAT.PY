import requests
import json

url = "https://api.p.2chat.io/open/whatsapp/send-message"

payload = json.dumps({
  "to_number": "+249122302757",
  "from_number": "+96898157645",
  "text": "Test from 2Chat API",
  "url": "https://uploads-ssl.webflow.com/6281a9c52303343ff7c3b269/62a1648ee0273340bf38e3a9_logo-2C.svg"
})
headers = {
  'X-User-API-Key': 'UAK38ea04e4-725f-49b6-8dfd-897cb61534f1',
  'Content-Type': 'application/json'
}

response = requests.request("POST", url, headers=headers, data=payload)

print(response.text)


**بوابة التواصل الذكية لشركة رواسي الاتقان للاستثمار**  
![Python Version](https://img.shields.io/badge/Python-3.10%2B-blue)  
![Meta API](https://img.shields.io/badge/Meta%20API-Approved-green)  


## المميزات الرئيسية 🚀

- نظام قوائم تفاعلية متعدد المراحل
- عرض الخدمات:
  - ✅ حلول تطوير البرمجيات المخصصة
  - ✅ تكامل واتساب بزنس API
  - ✅ إدارة الحملات التسويقية الذكية
- إدارة العملاء المحتملين (Leads) تلقائيًا
- دعم إرسال الملفات (PDF, صور، فيديو)
- ردود ذكية حسب سياق المحادثة  


## المتطلبات المسبقة 📋

- Python 3.10 أو أحدث
- حساب واتساب بزنس معتمد من ميتا
- [Ngrok](https://ngrok.com/) للتطوير المحلي
- معرفة أساسية بـ WhatsApp Business API  


## التثبيت 💻

```bash
# انسخ المشروع
git clone https://github.com/rawasy-alitqan/whatsapp-bot.git
cd whatsapp-bot

# أنشئ بيئة افتراضية
python -m venv venv
source venv/bin/activate  # لنكس/ماك
# .\venv\Scripts\activate  # ويندوز

# ثبت المكتبات المطلوبة
pip install flask pywa python-dotenv requests
```  


## ملف الإعدادات ⚙️

1. أنشئ ملف `.env`:
```env
WHATSAPP_PHONE_NUMBER_ID="رقم_الهاتف_التجاري"
WHATSAPP_ACCESS_TOKEN="رمز_الوصول_الخاص"
VERIFY_TOKEN="رمز_تحقق_سري"
```

2. **إعدادات ميتا للمطورين**:
   - أنشئ تطبيقًا جديدًا من [منصة ميتا](https://developers.facebook.com/)
   - أضف منتج واتساب بزنس API
   - اضبط الويب هوك:
     - رابط الويب هوك: `https://your-ngrok-url.ngrok.io/`
     - رمز التحقق: يجب أن يتطابق مع الملف `.env`

3. **تفعيل رقم واتساب**:
   - اربط رقم الهاتف التجاري عبر [Meta Business Suite](https://business.facebook.com/)
   - تأكد من تفعيل وضع المطور  


## طريقة الاستخدام 📲

1. **تشغيل البوت**:
```bash
python app.py
```

2. **تفاعل عبر واتساب**:
   - أرسل "قائمة" لعرض الخيارات الرئيسية
   - مثال لمحادثة:
     ```
     المستخدم: قائمة
     البوت: [يعرض أزرار الخدمات الرئيسية]
     المستخدم: الضغط على "خدمات التطوير"
     البوت: [يعرض تفاصيل خدمات التطوير]
     ```

3. **الأوامر الرئيسية**:
   - `قائمة`: عرض القائمة الرئيسية
   - `مساعدة`: الحصول على دعم فني
   - `تواصل`: التواصل مع فريق المبيعات  


## هيكل النظام 🌐

| المسار       | الطريقة | الوصف                |
|--------------|---------|----------------------|
| `/`          | GET     | فحص حالة النظام     |
| `/webhook`   | POST    | نقطة اتصال واتساب   |  


## التطوير المستقبلي 🔮

- [ ] دعم بوابة دفع إلكتروني
- [ ] تكامل مع أنظمة CRM
- [ ] لوحة تحكم إحصائية
- [ ] دعم اللغات المتعددة  


## الرخصة 📄

هذا المشروع مرخص تحت [MIT License](LICENSE).  


---

**للتواصل مع فريق رواسي الاتقان**:  
📱 +96898157645  
📧 info@rawasy-alitqan.com  
🌐 [https://rawasy-al-itqan.prof-dev.com](https://rawasy-al-itqan.prof-dev.com)  


![Rawasy Alitqan Logo](https://rawasy-al-itqan.prof-dev.com/logo.png)  


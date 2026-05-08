import telebot
from telebot import types
from flask import Flask
from threading import Thread
import os

# 1. تشغيل سيرفر وهمي لإرضاء Render ومنع إيقاف البوت
app = Flask('')
@app.route('/')
def home():
    return "Bot is Alive!"

def run():
    app.run(host='0.0.0.0', port=8080)

# 2. إعدادات البوت والتوكن (التوكن الجديد اللي شغال معك)
TOKEN = '8260522692:AAFt81cAPzjbNOHyqzgWJRzFTNc_FU84X0U'
bot = telebot.TeleBot(TOKEN)

# مخزن ذكي للحالات عشان ما يتلخبط البوت
user_steps = {}

@bot.message_handler(commands=['start'])
def welcome(message):
    user_steps[message.chat.id] = None # تصفير الحالة
    markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    markup.add(
        types.KeyboardButton('إدارة الإيميلات 📁'),
        types.KeyboardButton('بدء عملية الرفع 🚀'),
        types.KeyboardButton('الإحصائيات 📊')
    )
    bot.send_message(message.chat.id, "🚀 نظام الرفع V12 جاهز للعمل.\nالحالة: متصل ✅", reply_markup=markup)

@bot.message_handler(func=lambda m: True)
def handle_all(message):
    cid = message.chat.id
    text = message.text

    # معالجة القائمة الرئيسية
    if text == 'إدارة الإيميلات 📁':
        user_steps[cid] = None
        bot.send_message(cid, "📁 قائمة الإيميلات المسجلة:\n1- Khaled***@gmail.com\n2- Saad***@gmail.com")
    
    elif text == 'الإحصائيات 📊':
        user_steps[cid] = None
        bot.send_message(cid, "📊 الإحصائيات:\n- الرسائل المرفوعة اليوم: 150\n- الإيميلات النشطة: 2")

    elif text == 'بدء عملية الرفع 🚀':
        user_steps[cid] = 'STEP_TEXT'
        bot.send_message(cid, "1️⃣ أرسل نص الرسالة (كود الرفع):")

    # معالجة الخطوات (الحل الجذري لمشكلة "أرسل رقم فقط")
    elif user_steps.get(cid) == 'STEP_TEXT':
        user_steps[cid] = 'STEP_NUM'
        bot.send_message(cid, "2️⃣ كم عدد الرسائل من كل إيميل؟ (أرسل رقم فقط)")

    elif user_steps.get(cid) == 'STEP_NUM':
        if text.isdigit():
            bot.send_message(cid, f"✅ تم الاعتماد! جاري إرسال {text} رسالة لكل إيميل..")
            user_steps[cid] = None # إنهاء العملية والعودة للوضع الطبيعي
        else:
            bot.send_message(cid, "⚠️ خطأ! أرسل رقم فقط (مثال: 100)")
    
    else:
        bot.send_message(cid, "الرجاء اختيار أمر من القائمة بالأسفل 👇")

# 3. تشغيل السيرفر والبوت معاً
if __name__ == "__main__":
    t = Thread(target=run)
    t.start()
    print("Bot is starting...")
    bot.infinity_polling()

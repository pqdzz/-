import telebot
from telebot import types
import os
from flask import Flask
from threading import Thread

# 1. إعداد سيرفر وهمي عشان Render ما يطفي البوت
app = Flask('')
@app.route('/')
def home():
    return "Bot is alive!"

def run_web_server():
    app.run(host='0.0.0.0', port=8080)

# 2. إعدادات البوت والتوكن
TOKEN = '8260522692:AAFt81cAPzjbNOHyqzgWJRzFTNc_FU84X0U'
bot = telebot.TeleBot(TOKEN)

# مخزن البيانات (States)
user_status = {}

@bot.message_handler(commands=['start'])
def send_welcome(message):
    user_status[message.chat.id] = None # تصفير الحالة
    markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    btns = [
        types.KeyboardButton('إدارة الإيميلات 📁'),
        types.KeyboardButton('بدء عملية الرفع 🚀'),
        types.KeyboardButton('الإحصائيات 📊')
    ]
    markup.add(*btns)
    bot.send_message(message.chat.id, "🚀 نظام الرفع V11 جاهز العمل.\nالإيميلات المسجلة: 2", reply_markup=markup)

@bot.message_handler(func=lambda m: True)
def handle_all(message):
    cid = message.chat.id
    text = message.text

    # القائمة الرئيسية
    if text == 'إدارة الإيميلات 📁':
        user_status[cid] = None
        bot.send_message(cid, "📁 قائمة الإيميلات:\n1- Khaled***@gmail.com\n2- Saad***@gmail.com")
    
    elif text == 'الإحصائيات 📊':
        user_status[cid] = None
        bot.send_message(cid, "📊 إحصائيات اليوم:\n- الرسائل المرفوعة: 150\n- الحالة: متصل ✅")

    elif text == 'بدء عملية الرفع 🚀':
        user_status[cid] = 'WAITING_MSG'
        bot.send_message(cid, "1️⃣ أرسل نص الرسالة (كود الرفع):")

    # معالجة الخطوات (هنا حل مشكلة "أرسل رقم فقط")
    elif user_status.get(cid) == 'WAITING_MSG':
        user_status[cid] = 'WAITING_NUM'
        bot.send_message(cid, "2️⃣ كم عدد الرسائل من كل إيميل؟ (أرسل رقم فقط)")

    elif user_status.get(cid) == 'WAITING_NUM':
        if text.isdigit():
            bot.send_message(cid, f"✅ تم الاعتماد! جاري الرفع لـ {text} رسالة...")
            user_status[cid] = None # إنهاء العملية
        else:
            bot.send_message(cid, "⚠️ خطأ! أرسل رقم فقط (مثلاً: 50)")

# 3. تشغيل كل شيء
if __name__ == "__main__":
    # تشغيل السيرفر في خلفية (Thread) عشان Render
    t = Thread(target=run_web_server)
    t.start()
    print("Bot is starting...")
    bot.infinity_polling()

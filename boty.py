import telebot
from telebot import types

# التوكن الجديد حقك اللي شغال 100%
TOKEN = '8260522692:AAFt81cAPzjbNOHyqzgWJRzFTNc_FU84X0U'
bot = telebot.TeleBot(TOKEN)

# مخزن مؤقت لبيانات المستخدمين عشان ما تتداخل العمليات
user_data = {}

@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    itembtn1 = types.KeyboardButton('إدارة الإيميلات 📁')
    itembtn2 = types.KeyboardButton('بدء عملية الرفع 🚀')
    itembtn3 = types.KeyboardButton('الإحصائيات 📊')
    markup.add(itembtn1, itembtn2, itembtn3)
    
    bot.send_message(message.chat.id, "🚀 نظام الرفع V11 جاهز.\nالإيميلات المسجلة: 2", reply_markup=markup)

@bot.message_handler(func=lambda message: True)
def handle_messages(message):
    chat_id = message.chat.id
    
    if message.text == 'إدارة الإيميلات 📁':
        bot.send_message(chat_id, "📁 قائمة الإيميلات المسجلة:\n1- Khaled***@gmail.com\n2- Saad***@gmail.com")
        
    elif message.text == 'بدء عملية الرفع 🚀':
        user_data[chat_id] = {'step': 1}
        bot.send_message(chat_id, "1️⃣ أرسل نص الرسالة (كود الرفع):")
        
    elif message.text == 'الإحصائيات 📊':
        bot.send_message(chat_id, "📊 إحصائيات اليوم:\n- تم رفع: 150 رسالة\n- الإيميلات النشطة: 2")

    # هنا حل مشكلة "أرسل رقم فقط" - نتأكد إن المستخدم فعلاً في مرحلة إدخال بيانات
    elif chat_id in user_data:
        step = user_data[chat_id].get('step')
        
        if step == 1:
            user_data[chat_id]['text'] = message.text
            user_data[chat_id]['step'] = 2
            bot.send_message(chat_id, "2️⃣ كم عدد الرسائل من كل إيميل؟ (أرسل رقم فقط)")
            
        elif step == 2:
            if message.text.isdigit():
                num = message.text
                bot.send_message(chat_id, f"✅ تم البدء! جاري إرسال {num} رسالة بالنص المطلوب..")
                # هنا تنظف البيانات بعد ما تخلص العملية
                del user_data[chat_id]
            else:
                bot.send_message(chat_id, "⚠️ خطأ! أرسل رقم فقط (مثلاً: 10)")
    else:
        bot.send_message(chat_id, "الرجاء اختيار أمر من القائمة بالأسفل 👇")

# تشغيل البوت
print("Bot is running...")
bot.infinity_polling()

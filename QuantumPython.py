import telebot
import os
from telebot import types

# تنظیمات
TOKEN = os.getenv("BOT_TOKEN") 
MY_CHANNEL = "@Najm_5D"
TARGET_LINK = "https://t.me/mrKhabardar"
ADMIN_ID = 7801959849  # <--- حتماً آیدی عددی خودت را اینجا جایگزین صفر کن

bot = telebot.TeleBot(TOKEN)

def is_member(user_id):
    try:
        status = bot.get_chat_member(MY_CHANNEL, user_id).status
        return status in ['member', 'administrator', 'creator']
    except Exception as e:
        print(f"Error checking membership: {e}")
        return False

@bot.message_handler(commands=['start'])
def start_command(message):
    user_id = message.from_user.id
    user_name = message.from_user.first_name
    username = f"@{message.from_user.username}" if message.from_user.username else "بدون یوزرنیم"

    # --- قابلیت جدید: گزارش به ادمین ---
    try:
        report_msg = f"🚀 کاربر جدید ربات را استارت زد:\n\n👤 نام: {user_name}\n🆔 یوزرنیم: {username}\n🔢 آیدی عددی: {user_id}"
        bot.send_message(ADMIN_ID, report_msg)
    except:
        pass # اگر آیدی ادمین اشتباه باشد یا ربات را بلاک کرده باشد، برنامه کرش نمی‌کند
    # --------------------------------

    if is_member(user_id):
        bot.send_message(message.chat.id, f"✅ عضویت شما تایید شده است.\n\n🔗 لینک کانال مورد نظر:\n{TARGET_LINK}")
    else:
        markup = types.InlineKeyboardMarkup()
        btn_join = types.InlineKeyboardButton("📢 عضویت در کانال", url=f"https://t.me/{MY_CHANNEL.replace('@', '')}")
        btn_check = types.InlineKeyboardButton("🔄 تایید عضویت", callback_data="check_membership")
        markup.add(btn_join)
        markup.add(btn_check)

        bot.send_message(message.chat.id,
                         "👋 سلام به ربات Quantum خوش آمدید!\n\n⚠️ برای دسترسی به محتوا، ابتدا باید در کانال ما عضو شوید ",
                         reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data == "check_membership")
def check_callback(call):
    user_id = call.from_user.id

    if is_member(user_id):
        bot.edit_message_text(f"✅ با تشکر، عضویت شما تایید شد.\n\n🔗 لینک مقصد:\n{TARGET_LINK}",
                              call.message.chat.id,
                              call.message.message_id)
        bot.answer_callback_query(call.id, "خوش آمدید!")
    else:
        bot.answer_callback_query(call.id, "❌ شما هنوز در کانال @Najm_5D عضو نشده‌اید!", show_alert=True)

print("Quantum Bot is running...")
bot.infinity_polling()

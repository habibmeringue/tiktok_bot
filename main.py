import telebot
import requests
from flask import Flask, request
import threading

API_TOKEN = "7803378809:AAGVqEQBpxKeOUMY9vOdtRoHZaNMWqmgwIU"
bot = telebot.TeleBot(API_TOKEN)
ALLOWED_USERS = [1563478070]  # Replace with your own Telegram user ID

app = Flask(__name__)

def download_tiktok_video(url):
    api_url = f"https://api.tikwm.com/video/info?url={url}"
    res = requests.get(api_url)
    if res.status_code != 200:
        return None, "⛔️ فشل في الاتصال بالخدمة."
    data = res.json()
    if not data.get("data") or not data["data"].get("play"):
        return None, "⛔️ الفيديو غير متاح."
    return data["data"]["play"], None

@bot.message_handler(commands=["start"])
def send_welcome(message):
    bot.reply_to(message, "👋 أرسل رابط TikTok لتحميل الفيديو.")

@bot.message_handler(commands=["id"])
def get_user_id(message):
    bot.reply_to(message, f"🆔 User ID: {message.from_user.id}")

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    if message.from_user.id not in ALLOWED_USERS:
        bot.reply_to(message, "🚫 لا تملك صلاحية استعمال البوت.")
        return

    url = message.text.strip()
    if "tiktok.com" not in url:
        bot.reply_to(message, "⛔️ أرسل رابط TikTok صحيح.")
        return

    video_url, error = download_tiktok_video(url)
    if error:
        bot.reply_to(message, error)
        return

    video = requests.get(video_url)
    bot.send_video(message.chat.id, video.content, caption="✅ الفيديو بلا علامة مائية.")

@app.route("/")
def home():
    return "OK"

def run_flask():
    app.run(host="0.0.0.0", port=3000)

def run_bot():
    bot.polling()

if __name__ == "__main__":
    threading.Thread(target=run_flask).start()
    run_bot()

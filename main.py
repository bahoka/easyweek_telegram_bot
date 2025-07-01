# main.py
import json
import os
import requests
import asyncio
import subprocess
from flask import Flask, request, jsonify
from threading import Thread
from telegram import Update, KeyboardButton, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

TELEGRAM_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
USERS_FILE = "users.json"

app = Flask(__name__)

def load_users():
    if os.path.exists(USERS_FILE):
        with open(USERS_FILE, "r") as f:
            return json.load(f)
    return {}

def save_users(data):
    with open(USERS_FILE, "w") as f:
        json.dump(data, f)

def send_telegram_message(chat_id, text):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    requests.post(url, json={"chat_id": chat_id, "text": text})

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.json
    phone = data.get("phone") or data.get("client", {}).get("phone")
    if not phone:
        return jsonify({"error": "Phone not found"}), 400

    phone = phone.replace(" ", "").replace("+", "").replace("-", "")
    users = load_users()
    tg_id = users.get(phone)
    if tg_id:
        service = data.get("service", {}).get("name", "услуга")
        time = data.get("start", "время не указано")
        msg = f"📅 Вы записаны на {service} в {time}"
        send_telegram_message(tg_id, msg)

    return jsonify({"status": "ok"}), 200

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    button = KeyboardButton("Поделиться номером", request_contact=True)
    keyboard = ReplyKeyboardMarkup([[button]], resize_keyboard=True, one_time_keyboard=True)
    await update.message.reply_text("Пожалуйста, поделитесь номером телефона", reply_markup=keyboard)

async def contact_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    contact = update.message.contact
    phone = contact.phone_number.replace(" ", "").replace("+", "").replace("-", "")
    user_id = update.effective_user.id
    users = load_users()
    users[phone] = user_id
    save_users(users)
    await update.message.reply_text("✅ Спасибо! Вы будете получать уведомления о записях.")

def run_bot():
    asyncio.set_event_loop(asyncio.new_event_loop())  # ✅ создаём loop в потоке
    app_tg = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    app_tg.add_handler(CommandHandler("start", start))
    app_tg.add_handler(MessageHandler(filters.CONTACT, contact_handler))
    app_tg.run_polling()

if __name__ == "__main__":
    Thread(target=run_bot).start()
    subprocess.Popen(["python", "bot.py"])
    app.run(host="0.0.0.0", port=5000)

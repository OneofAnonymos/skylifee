from telegram import Update
from telegram.ext import ContextTypes, CommandHandler, Application
from db import connect
import random

events = [
    {"text": "👛 کیف پولی پیدا کردی و داخلش 100 سکه بود!", "money": 100, "xp": 10, "energy": 0, "happy": 5},
    {"text": "🤒 ناگهان سرما خوردی! باید استراحت کنی.", "money": -50, "xp": -5, "energy": -20, "happy": -10},
    {"text": "🎁 یه نفر بهت یه هدیه داد! خوشحال شدی.", "money": 0, "xp": 15, "energy": 0, "happy": 15},
    {"text": "👞 کفش‌هات پاره شد و باید یکی دیگه بخری.", "money": -70, "xp": 0, "energy": 0, "happy": -5},
    {"text": "💡 یه ایده جالب برای استارتاپ به ذهنت رسید و 50 XP گرفتی!", "money": 0, "xp": 50, "energy": -10, "happy": 10},
    {"text": "🚑 تصادف کوچیکی کردی و باید به دکتر بری.", "money": -100, "xp": -10, "energy": -30, "happy": -20},
    {"text": "🍀 بخت با تو یار بود! یک آیتم رایگان بردی.", "money": 0, "xp": 0, "energy": 0, "happy": 10},
]

async def random_event(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    event = random.choice(events)

    conn = connect()
    c = conn.cursor()

    # بروزرسانی پروفایل
    c.execute("""
        UPDATE profiles 
        SET money = money + ?, xp = xp + ?, energy = energy + ?, happiness = happiness + ?
        WHERE user_id = ?
    """, (event["money"], event["xp"], event["energy"], event["happy"], user_id))

    conn.commit()
    conn.close()

    await update.message.reply_text(f"🎲 رویداد شانسی:\n{event['text']}")

def register(app: Application):
    app.add_handler(CommandHandler("event", random_event))
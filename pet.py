from telegram import Update
from telegram.ext import ContextTypes, CommandHandler, Application
from db import connect
import random

pet_names = ["مینی", "لوکی", "پوچی", "برفی", "چیکو", "زئوس", "رایا", "آلفا"]

def get_pet(user_id):
    conn = connect()
    c = conn.cursor()
    c.execute("SELECT name, happiness, level FROM pets WHERE user_id = ?", (user_id,))
    pet = c.fetchone()
    conn.close()
    return pet

async def adopt_pet(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if get_pet(user_id):
        await update.message.reply_text("🐾 تو قبلاً یه حیوان داری!")
        return

    pet_name = random.choice(pet_names)
    conn = connect()
    c = conn.cursor()
    c.execute("INSERT INTO pets (user_id, name, happiness, level) VALUES (?, ?, ?, ?)",
              (user_id, pet_name, 50, 1))
    conn.commit()
    conn.close()
    await update.message.reply_text(f"🎉 تبریک! حیوان خانگی جدیدت {pet_name} نام داره!")

async def feed_pet(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    pet = get_pet(user_id)
    if not pet:
        await update.message.reply_text("🐾 هنوز حیوانی نداری. با /adopt_pet یکی بگیر.")
        return

    conn = connect()
    c = conn.cursor()
    c.execute("UPDATE pets SET happiness = MIN(happiness + 10, 100) WHERE user_id = ?", (user_id,))
    conn.commit()
    conn.close()
    await update.message.reply_text("🍗 به حیوانت غذا دادی! خوشحال‌تر شد.")

async def pet_info(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    pet = get_pet(user_id)
    if not pet:
        await update.message.reply_text("🐾 هنوز حیوانی نداری.")
        return

    name, happiness, level = pet
    await update.message.reply_text(f"""🐶 اطلاعات حیوانت:
📛 نام: {name}
😊 خوشحالی: {happiness} / 100
⭐ سطح: {level}""")

def register(app: Application):
    app.add_handler(CommandHandler("adopt_pet", adopt_pet))
    app.add_handler(CommandHandler("feed_pet", feed_pet))
    app.add_handler(CommandHandler("pet", pet_info))
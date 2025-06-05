from telegram import Update
from telegram.ext import ContextTypes, CommandHandler, Application
from db import connect
import random

async def sleep(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    conn = connect()
    c = conn.cursor()

    c.execute("SELECT energy, happiness FROM profiles WHERE user_id = ?", (user_id,))
    row = c.fetchone()
    if not row:
        await update.message.reply_text("⚠️ اول با دستور /start ثبت‌نام کن.")
        return

    new_energy = min(row[0] + 30, 100)
    new_happiness = min(row[1] + 10, 100)

    c.execute("UPDATE profiles SET energy = ?, happiness = ?, sleep = 0 WHERE user_id = ?",
              (new_energy, new_happiness, user_id))
    conn.commit()
    conn.close()

    await update.message.reply_text("😴 خوابیدی و استراحت کردی. انرژی و شادی‌ات بیشتر شد!")

async def eat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    conn = connect()
    c = conn.cursor()

    c.execute("SELECT hunger, money FROM profiles WHERE user_id = ?", (user_id,))
    row = c.fetchone()
    if not row:
        await update.message.reply_text("⚠️ با /start ثبت‌نام کن.")
        return

    if row[1] < 20:
        await update.message.reply_text("💸 پول کافی برای غذا نداری.")
        return

    new_hunger = max(row[0] - 30, 0)
    c.execute("UPDATE profiles SET hunger = ?, money = money - 20 WHERE user_id = ?",
              (new_hunger, user_id))
    conn.commit()
    conn.close()

    await update.message.reply_text("🍽️ غذا خوردی و گرسنگی‌ات کمتر شد.")

async def take_medicine(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    conn = connect()
    c = conn.cursor()

    c.execute("SELECT health, money FROM profiles WHERE user_id = ?", (user_id,))
    row = c.fetchone()
    if not row:
        await update.message.reply_text("⚠️ اول با /start ثبت‌نام کن.")
        return

    if row[0] == 1:
        await update.message.reply_text("✅ تو سالمی و نیازی به دارو نداری.")
        return

    if row[1] < 50:
        await update.message.reply_text("💸 پول کافی برای دارو نداری.")
        return

    c.execute("UPDATE profiles SET health = 1, money = money - 50 WHERE user_id = ?", (user_id,))
    conn.commit()
    conn.close()

    await update.message.reply_text("💊 دارو خوردی و حالت بهتر شد.")

async def random_illness_event(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if random.random() < 0.1:  # 10% احتمال مریض شدن
        conn = connect()
        c = conn.cursor()
        c.execute("UPDATE profiles SET health = 0 WHERE user_id = ?", (user_id,))
        conn.commit()
        conn.close()
        await update.message.reply_text("🤒 اوه نه! مریض شدی! با /medicine درمان کن.")

def register(app: Application):
    app.add_handler(CommandHandler("sleep", sleep))
    app.add_handler(CommandHandler("eat", eat))
    app.add_handler(CommandHandler("medicine", take_medicine))
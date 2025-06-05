from telegram import Update
from telegram.ext import ContextTypes, CommandHandler, Application
from db import connect
import random

async def battle(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if not context.args:
        await update.message.reply_text("⚔️ استفاده صحیح: /battle @username")
        return

    opponent_username = context.args[0].lstrip('@')
    conn = connect()
    c = conn.cursor()

    # اطلاعات کاربر
    c.execute("SELECT xp, energy, happiness FROM profiles WHERE user_id = ?", (user_id,))
    user = c.fetchone()
    if not user or user[1] < 20:
        await update.message.reply_text("❌ انرژی کافی برای مبارزه نداری (حداقل ۲۰ نیاز است).")
        return

    # اطلاعات حریف
    c.execute("SELECT user_id, xp, energy, happiness FROM profiles WHERE username = ?", (opponent_username,))
    opponent = c.fetchone()
    if not opponent:
        await update.message.reply_text("❌ حریف مورد نظر پیدا نشد.")
        return

    opponent_id, opp_xp, opp_energy, opp_happiness = opponent
    if opp_energy < 20:
        await update.message.reply_text("❌ حریف انرژی کافی برای مبارزه ندارد.")
        return

    # شانس برد بر اساس xp
    user_score = user[0] + random.randint(0, 50)
    opp_score = opp_xp + random.randint(0, 50)

    if user_score > opp_score:
        result = f"🏆 تو برنده شدی! (+20 XP)"
        c.execute("UPDATE profiles SET xp = xp + 20, energy = energy - 20, happiness = happiness + 5 WHERE user_id = ?", (user_id,))
        c.execute("UPDATE profiles SET energy = energy - 20, happiness = happiness - 5 WHERE user_id = ?", (opponent_id,))
    elif user_score < opp_score:
        result = f"😢 باختی! (+10 XP)"
        c.execute("UPDATE profiles SET xp = xp + 10, energy = energy - 20, happiness = happiness - 5 WHERE user_id = ?", (user_id,))
        c.execute("UPDATE profiles SET energy = energy - 20, happiness = happiness + 5 WHERE user_id = ?", (opponent_id,))
    else:
        result = "🤝 مساوی شد! (+15 XP)"
        c.execute("UPDATE profiles SET xp = xp + 15, energy = energy - 20 WHERE user_id IN (?, ?)", (user_id, opponent_id))

    conn.commit()
    conn.close()

    await update.message.reply_text(f"{result}\n📊 امتیاز تو: {user_score} | امتیاز حریف: {opp_score}")

def register(app: Application):
    app.add_handler(CommandHandler("battle", battle))
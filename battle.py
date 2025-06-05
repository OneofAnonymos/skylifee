from telegram import Update
from telegram.ext import CommandHandler, ContextTypes
import db

async def fight(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    user = db.get_user(user_id)
    
    if not user:
        await update.message.reply_text("شما هنوز ثبت‌نام نکردید.")
        return

    xp_gain = 10
    db.update_user(user_id, "xp", user["xp"] + xp_gain)
    await update.message.reply_text(f"شما وارد یک مبارزه شدید و {xp_gain} XP گرفتید!")

async def show_ranking(update: Update, context: ContextTypes.DEFAULT_TYPE):
    top_users = db.get_top_users()
    message = "🏆 رتبه‌بندی کاربران:\n"
    for i, user in enumerate(top_users, start=1):
        message += f"{i}. {user['name']} - Level {user['level']} - XP {user['xp']}\n"
    await update.message.reply_text(message)

def register(app):
    app.add_handler(CommandHandler("fight", fight))
    app.add_handler(CommandHandler("ranking", show_ranking))

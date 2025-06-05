from telegram import Update
from telegram.ext import ContextTypes, Application, CommandHandler
from db import connect

skill_list = {
    "موسیقی": {"energy": 10, "xp": 15},
    "برنامه‌نویسی": {"energy": 15, "xp": 25},
    "ورزش": {"energy": 12, "xp": 20},
}

async def learn(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    if len(context.args) == 0:
        skills = "\n".join([f"🎯 {name}" for name in skill_list])
        await update.message.reply_text(f"برای آموزش، یکی از مهارت‌های زیر را انتخاب کن:\n\n{skills}\n\nمثال: /learn موسیقی")
        return

    skill = context.args[0]
    if skill not in skill_list:
        await update.message.reply_text("❌ این مهارت وجود ندارد. لطفاً یکی از مهارت‌های مشخص‌شده را انتخاب کن.")
        return

    conn = connect()
    c = conn.cursor()

    c.execute("SELECT energy, xp FROM profiles WHERE user_id = ?", (user.id,))
    row = c.fetchone()

    if not row:
        await update.message.reply_text("⚠️ ابتدا با /start ثبت‌نام کن.")
        conn.close()
        return

    energy, xp = row
    need = skill_list[skill]["energy"]
    gain = skill_list[skill]["xp"]

    if energy < need:
        await update.message.reply_text("😫 انرژی کافی برای یادگیری نداری.")
        conn.close()
        return

    c.execute("UPDATE profiles SET energy = energy - ?, xp = xp + ? WHERE user_id = ?", (need, gain, user.id))
    conn.commit()
    conn.close()

    await update.message.reply_text(f"📚 شما مهارت {skill} را تمرین کردید!\n⚡ -{need} انرژی\n⭐ +{gain} XP")

def register(app: Application):
    app.add_handler(CommandHandler("learn", learn))
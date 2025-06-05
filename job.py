from telegram import Update
from telegram.ext import ContextTypes, Application, CommandHandler
from db import connect

jobs = {
    "هیچ‌کاره": {"income": 0, "next": "کارگر"},
    "کارگر": {"income": 50, "next": "فروشنده"},
    "فروشنده": {"income": 100, "next": "برنامه‌نویس"},
    "برنامه‌نویس": {"income": 200, "next": "مدیر پروژه"},
    "مدیر پروژه": {"income": 300, "next": None}
}

async def choose_job(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    conn = connect()
    c = conn.cursor()

    c.execute("SELECT job FROM profiles WHERE user_id = ?", (user.id,))
    row = c.fetchone()

    if row:
        current_job = row[0] or "هیچ‌کاره"
        if current_job not in jobs:
            current_job = "هیچ‌کاره"
        next_job = jobs[current_job]["next"]
        if next_job:
            c.execute("UPDATE profiles SET job = ? WHERE user_id = ?", (next_job, user.id))
            conn.commit()
            await update.message.reply_text(f"🎉 تبریک! شغل جدید شما: {next_job}")
        else:
            await update.message.reply_text("🔝 شما در بالاترین سطح شغلی هستید.")
    else:
        await update.message.reply_text("⚠️ ابتدا با /start ثبت‌نام کنید.")

    conn.close()

async def work(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    conn = connect()
    c = conn.cursor()

    c.execute("SELECT job, energy, money FROM profiles WHERE user_id = ?", (user.id,))
    row = c.fetchone()

    if not row:
        await update.message.reply_text("⚠️ ابتدا با /start ثبت‌نام کنید.")
        return

    job, energy, money = row
    if not job or job not in jobs or job == "هیچ‌کاره":
        await update.message.reply_text("❌ شما شغلی ندارید! با دستور /job شغلی انتخاب کنید.")
        return

    if energy < 10:
        await update.message.reply_text("🥱 انرژی کافی برای کار کردن نداری! بخواب یا غذا بخور.")
        return

    income = jobs[job]["income"]
    c.execute("UPDATE profiles SET money = money + ?, energy = energy - 10 WHERE user_id = ?", (income, user.id))
    conn.commit()

    await update.message.reply_text(f"💼 شما به عنوان {job} کار کردید و {income} سکه دریافت کردید! (⚡ -10 انرژی)")

    conn.close()

def register(app: Application):
    app.add_handler(CommandHandler("job", choose_job))
    app.add_handler(CommandHandler("work", work))
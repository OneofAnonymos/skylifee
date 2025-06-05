from telegram import Update
from telegram.ext import ContextTypes, Application
from db import connect

async def create_profile(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    conn = connect()
    c = conn.cursor()

    c.execute("SELECT * FROM profiles WHERE user_id = ?", (user.id,))
    if c.fetchone():
        await update.message.reply_text("✅ شما قبلاً ثبت‌نام کرده‌اید. با دستور /profile وضعیت خود را ببینید.")
    else:
        c.execute(
            "INSERT INTO profiles (user_id, username) VALUES (?, ?)",
            (user.id, user.username or "Unknown")
        )
        conn.commit()
        await update.message.reply_text("🎉 پروفایل شما با موفقیت ساخته شد! با دستور /profile مشاهده‌اش کن.")

    conn.close()

async def show_profile(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    conn = connect()
    c = conn.cursor()

    c.execute("SELECT * FROM profiles WHERE user_id = ?", (user.id,))
    row = c.fetchone()

    if row:
        text = (
            f"👤 پروفایل شما:\n"
            f"🏷️ نام: @{row[1]}\n"
            f"💰 پول: {row[2]} سکه\n"
            f"🎚️ سطح: {row[3]}\n"
            f"⭐ XP: {row[4]}\n"
            f"⚡ انرژی: {row[5]}\n"
            f"😊 شادی: {row[6]}\n"
            f"😴 خواب: {row[7]}\n"
            f"🍗 گرسنگی: {row[8]}\n"
            f"🏙️ شهر فعلی: {row[9]}\n"
            f"💼 شغل: {row[10] or 'نداری!'}\n"
            f"❤️ متأهل با: {row[11] if row[11] else 'نداری'}"
        )
        await update.message.reply_text(text)
    else:
        await update.message.reply_text("⚠️ اول باید با /start ثبت‌نام کنی.")

    conn.close()

async def show_status(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    conn = connect()
    c = conn.cursor()

    c.execute("SELECT energy, happiness, sleep, hunger FROM profiles WHERE user_id = ?", (user.id,))
    row = c.fetchone()

    if row:
        text = (
            f"📊 وضعیت فعلی شما:\n"
            f"⚡ انرژی: {row[0]}\n"
            f"😊 شادی: {row[1]}\n"
            f"😴 خواب: {row[2]}\n"
            f"🍗 گرسنگی: {row[3]}"
        )
        await update.message.reply_text(text)
    else:
        await update.message.reply_text("⚠️ اول با /start ثبت‌نام کن.")

    conn.close()

def register(app: Application):
    app.add_handler(CommandHandler("profile", show_profile))
    app.add_handler(CommandHandler("status", show_status))
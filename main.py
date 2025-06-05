import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

import profile
import job
import skills
import travel
import items
import actions
import relationships
import battle
import pet
import events

from db import init_db
from secrets import TOKEN  # توکنت رو توی فایل secrets.py قرار بده

# لاگ‌ها برای دیباگ
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# شروع ربات
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await profile.create_profile(update, context)

# راهنما
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👤 /profile - مشاهده پروفایل\n"
        "📈 /status - وضعیت شخصیت\n"
        "💼 /job - شغل فعلی\n"
        "💵 /work - کار کردن\n"
        "🧠 /train - آموزش مهارت\n"
        "🧳 /travel - سفر به شهر دیگر\n"
        "🏬 /shop - فروشگاه\n"
        "🎒 /inventory - موجودی آیتم‌ها\n"
        "🛌 /sleep - خوابیدن\n"
        "🍔 /eat - غذا خوردن\n"
        "💊 /medicine - استفاده از دارو\n"
        "💍 /marry - ازدواج با دیگران\n"
        "🎁 /gift - هدیه دادن\n"
        "⚔️ /fight - مبارزه با دیگران\n"
        "🐶 /pet - وضعیت حیوان خانگی\n"
        "🎲 /event - رویداد شانسی\n"
        "🏆 /ranking - رتبه‌بندی\n"
        "❓ /help - نمایش راهنما"
    )

# اجرای ربات
def main():
    init_db()
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))

    # ثبت همه ماژول‌ها
    profile.register(app)
    job.register(app)
    skills.register(app)
    travel.register(app)
    items.register(app)
    actions.register(app)
    relationships.register(app)
    battle.register(app)
    pet.register(app)
    events.register(app)

    app.run_polling()

if __name__ == '__main__':
    main()
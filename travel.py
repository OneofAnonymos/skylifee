from telegram import Update
from telegram.ext import ContextTypes, Application, CommandHandler
from db import connect
import random

cities = {
    "تهران": 0,
    "شیراز": 100,
    "اصفهان": 150,
    "مشهد": 200,
    "تبریز": 250,
    "کیش": 300,
    "رشت": 180,
    "یزد": 120
}

async def travel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    conn = connect()
    c = conn.cursor()

    c.execute("SELECT money, location, energy FROM profiles WHERE user_id = ?", (user.id,))
    row = c.fetchone()

    if not row:
        await update.message.reply_text("⚠️ ابتدا با /start ثبت‌نام کن.")
        return

    money, current_city, energy = row

    if len(context.args) == 0:
        city_list = "\n".join([f"🌆 {city} - 💰{cost} سکه" for city, cost in cities.items()])
        await update.message.reply_text(f"شهر مقصد را مشخص کن:\n\n{city_list}\n\nمثال: /travel مشهد")
        return

    dest = context.args[0]
    if dest not in cities:
        await update.message.reply_text("❌ این شهر وجود ندارد.")
        return

    cost = cities[dest]
    if dest == current_city:
        await update.message.reply_text("⛔ شما هم‌اکنون در همین شهر هستید!")
        return

    if money < cost:
        await update.message.reply_text("💸 پول کافی برای سفر نداری!")
        return

    if energy < 15:
        await update.message.reply_text("🥱 انرژی کافی برای سفر نداری! (حداقل ۱۵)")
        return

    c.execute("UPDATE profiles SET location = ?, money = money - ?, energy = energy - 15 WHERE user_id = ?",
              (dest, cost, user.id))
    conn.commit()

    message = f"🧳 شما به {dest} سفر کردید!\n💰 -{cost} سکه | ⚡ -15 انرژی"

    # رویداد تصادفی در سفر
    event = random.choice(["", "🎁 شما یک آیتم رایگان پیدا کردید!", "💀 شما بیمار شدید و نیاز به دارو دارید!", "💰 کسی به شما ۵۰ سکه هدیه داد!"])
    if event == "💰 کسی به شما ۵۰ سکه هدیه داد!":
        c.execute("UPDATE profiles SET money = money + 50 WHERE user_id = ?", (user.id,))
        conn.commit()
    elif event == "💀 شما بیمار شدید و نیاز به دارو دارید!":
        c.execute("UPDATE profiles SET health = 0 WHERE user_id = ?", (user.id,))
        conn.commit()

    if event:
        message += f"\n\n❗ رویداد سفر: {event}"

    await update.message.reply_text(message)
    conn.close()

def register(app: Application):
    app.add_handler(CommandHandler("travel", travel))
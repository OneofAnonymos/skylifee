from telegram import Update
from telegram.ext import ContextTypes, Application, CommandHandler
from db import connect

items = {
    "غذا": {"price": 30, "energy": 10, "hunger": -20},
    "دارو": {"price": 50, "health": 1},
    "خانه کوچک": {"price": 500, "type": "house"},
    "خانه ویلایی": {"price": 1500, "type": "house"},
    "کتاب برنامه‌نویسی": {"price": 100, "xp": 20},
}

async def shop(update: Update, context: ContextTypes.DEFAULT_TYPE):
    item_list = "\n".join([f"🛒 {name} - 💰{data['price']}" for name, data in items.items()])
    await update.message.reply_text(f"📦 لیست آیتم‌ها:\n\n{item_list}\n\nبرای خرید: /buy <نام آیتم>\nبرای فروش: /sell <نام آیتم>")

async def buy(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if len(context.args) == 0:
        await update.message.reply_text("🛍️ لطفاً نام آیتمی را وارد کن. مثال: /buy غذا")
        return

    item = context.args[0]
    if item not in items:
        await update.message.reply_text("❌ آیتم مورد نظر پیدا نشد.")
        return

    conn = connect()
    c = conn.cursor()
    user_id = update.effective_user.id
    c.execute("SELECT money FROM profiles WHERE user_id = ?", (user_id,))
    row = c.fetchone()

    if not row:
        await update.message.reply_text("⚠️ ابتدا با /start ثبت‌نام کن.")
        conn.close()
        return

    money = row[0]
    price = items[item]["price"]
    if money < price:
        await update.message.reply_text("💸 پول کافی نداری!")
        conn.close()
        return

    # کاهش پول و اعمال آیتم
    c.execute("UPDATE profiles SET money = money - ? WHERE user_id = ?", (price, user_id))
    if "energy" in items[item]:
        c.execute("UPDATE profiles SET energy = MIN(energy + ?, 100) WHERE user_id = ?", (items[item]["energy"], user_id))
    if "hunger" in items[item]:
        c.execute("UPDATE profiles SET hunger = MAX(hunger + ?, 0) WHERE user_id = ?", (items[item]["hunger"], user_id))
    if "health" in items[item]:
        c.execute("UPDATE profiles SET health = 1 WHERE user_id = ?", (user_id,))
    if "xp" in items[item]:
        c.execute("UPDATE profiles SET xp = xp + ? WHERE user_id = ?", (items[item]["xp"], user_id))
    if items[item].get("type") == "house":
        c.execute("UPDATE profiles SET house = ? WHERE user_id = ?", (item, user_id))

    conn.commit()
    conn.close()
    await update.message.reply_text(f"✅ آیتم {item} خریداری شد.")

async def sell(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if len(context.args) == 0:
        await update.message.reply_text("🪙 لطفاً نام آیتمی که می‌خواهی بفروشی وارد کن. مثال: /sell غذا")
        return

    item = context.args[0]
    if item not in items:
        await update.message.reply_text("❌ این آیتم در لیست فروش نیست.")
        return

    price = int(items[item]["price"] * 0.5)

    conn = connect()
    c = conn.cursor()
    user_id = update.effective_user.id

    # برای ساده‌سازی فرض می‌کنیم کاربر آیتم را داشته (نیاز به سیستم اینونتوری نداریم فعلاً)
    c.execute("UPDATE profiles SET money = money + ? WHERE user_id = ?", (price, user_id))
    conn.commit()
    conn.close()

    await update.message.reply_text(f"🪙 آیتم {item} به قیمت {price} سکه فروخته شد.")

def register(app: Application):
    app.add_handler(CommandHandler("shop", shop))
    app.add_handler(CommandHandler("buy", buy))
    app.add_handler(CommandHandler("sell", sell))
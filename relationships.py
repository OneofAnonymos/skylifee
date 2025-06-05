from telegram import Update
from telegram.ext import ContextTypes, CommandHandler, Application
from db import connect

async def marry(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if not context.args:
        await update.message.reply_text("💍 باید به کسی ریپلای بزنی یا آی‌دی بدی: /marry @username")
        return

    partner_username = context.args[0].lstrip('@')

    conn = connect()
    c = conn.cursor()

    c.execute("SELECT * FROM profiles WHERE user_id = ?", (user_id,))
    if not c.fetchone():
        await update.message.reply_text("⚠️ با /start ثبت‌نام کن.")
        return

    c.execute("SELECT user_id FROM profiles WHERE username = ?", (partner_username,))
    partner = c.fetchone()
    if not partner:
        await update.message.reply_text("❌ کاربر مورد نظر پیدا نشد.")
        return

    partner_id = partner[0]

    c.execute("UPDATE profiles SET partner = ? WHERE user_id = ?", (partner_id, user_id))
    c.execute("UPDATE profiles SET partner = ? WHERE user_id = ?", (user_id, partner_id))
    conn.commit()
    conn.close()

    await update.message.reply_text(f"🎉 تبریک! تو با @{partner_username} ازدواج کردی!")

async def divorce(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    conn = connect()
    c = conn.cursor()
    c.execute("SELECT partner FROM profiles WHERE user_id = ?", (user_id,))
    result = c.fetchone()
    if not result or result[0] is None:
        await update.message.reply_text("❌ تو با کسی ازدواج نکردی.")
        return

    partner_id = result[0]
    c.execute("UPDATE profiles SET partner = NULL WHERE user_id IN (?, ?)", (user_id, partner_id))
    conn.commit()
    conn.close()
    await update.message.reply_text("💔 شما از هم جدا شدید.")

async def gift(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if len(context.args) < 2:
        await update.message.reply_text("🎁 استفاده صحیح: /gift @username مقدار")
        return

    target_username = context.args[0].lstrip('@')
    try:
        amount = int(context.args[1])
    except ValueError:
        await update.message.reply_text("❌ مقدار نامعتبر.")
        return

    conn = connect()
    c = conn.cursor()
    c.execute("SELECT money FROM profiles WHERE user_id = ?", (user_id,))
    giver = c.fetchone()
    if not giver or giver[0] < amount:
        await update.message.reply_text("❌ پول کافی نداری.")
        return

    c.execute("SELECT user_id FROM profiles WHERE username = ?", (target_username,))
    target = c.fetchone()
    if not target:
        await update.message.reply_text("❌ کاربر مورد نظر پیدا نشد.")
        return

    target_id = target[0]

    c.execute("UPDATE profiles SET money = money - ? WHERE user_id = ?", (amount, user_id))
    c.execute("UPDATE profiles SET money = money + ? WHERE user_id = ?", (amount, target_id))
    conn.commit()
    conn.close()

    await update.message.reply_text(f"🎁 تو به @{target_username} مبلغ {amount} سکه هدیه دادی!")

async def party(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    cost = 100
    conn = connect()
    c = conn.cursor()

    c.execute("SELECT money, happiness FROM profiles WHERE user_id = ?", (user_id,))
    result = c.fetchone()
    if not result:
        await update.message.reply_text("⚠️ با /start ثبت‌نام کن.")
        return

    if result[0] < cost:
        await update.message.reply_text("❌ پول کافی برای برگزاری مهمانی نداری.")
        return

    new_happiness = min(result[1] + 25, 100)
    c.execute("UPDATE profiles SET money = money - ?, happiness = ? WHERE user_id = ?",
              (cost, new_happiness, user_id))
    conn.commit()
    conn.close()

    await update.message.reply_text("🎊 مهمانی گرفتی و خوشحال‌تر شدی!")

def register(app: Application):
    app.add_handler(CommandHandler("marry", marry))
    app.add_handler(CommandHandler("divorce", divorce))
    app.add_handler(CommandHandler("gift", gift))
    app.add_handler(CommandHandler("party", party))
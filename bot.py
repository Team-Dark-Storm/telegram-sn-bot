from telegram.ext import ApplicationBuilder, MessageHandler, filters
import sqlite3
import os

# إنشاء قاعدة البيانات
db = sqlite3.connect("sn.db", check_same_thread=False)
cur = db.cursor()
cur.execute("CREATE TABLE IF NOT EXISTS sn (value TEXT UNIQUE)")
db.commit()

BOT_TOKEN = os.environ.get("8515898760:AAGRz4Sf00qZM0E74Agd1vUEfMUYKirt0zo")  # هنتعامل مع التوكن كـ Environment Variable

async def save_sn(update, context):
    sn = update.message.text.strip()

    try:
        cur.execute("INSERT INTO sn VALUES (?)", (sn,))
        db.commit()
        await update.message.reply_text("✅ SN اتسجل")
    except:
        await update.message.reply_text("⚠️ SN موجود قبل كدا")

app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, save_sn))

print("Bot is running...")
app.run_polling()

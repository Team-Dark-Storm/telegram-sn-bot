from telegram.ext import ApplicationBuilder, MessageHandler, filters
import sqlite3
import os
import re

# إنشاء قاعدة البيانات
db = sqlite3.connect("sn.db", check_same_thread=False)
cur = db.cursor()
cur.execute("CREATE TABLE IF NOT EXISTS sn (value TEXT UNIQUE)")
db.commit()

# قراءة التوكن من Environment Variable
BOT_TOKEN = os.environ.get("BOT_TOKEN")

# دالة للتحقق من صحة SN
def is_valid_sn(sn):
    # طول من 8 لـ 12، أرقام + أحرف كبيرة فقط
    pattern = r"^[A-Z0-9]{8,12}$"
    return re.match(pattern, sn) is not None

# دالة استقبال الرسائل
async def save_sn(update, context):
    sn = update.message.text.strip().upper()  # تحويل لأي حرف كبير

    if not is_valid_sn(sn):
        await update.message.reply_text("⚠️ SN غير صالح! لازم يكون 8-12 حرف/رقم وكله Capital Letters")
        return

    try:
        cur.execute("INSERT INTO sn VALUES (?)", (sn,))
        db.commit()
        await update.message.reply_text("✅ SN اتسجل")
    except sqlite3.IntegrityError:
        await update.message.reply_text("⚠️ SN موجود قبل كدا")

# إعداد البوت
app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, save_sn))

print("Bot is running...")
app.run_polling()

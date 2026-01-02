import json
import os
import re
import threading
from flask import Flask, request
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# =========================
# إعدادات
# =========================
BOT_TOKEN = "8515898760:AAGRz4Sf00qZM0E74Agd1vUEfMUYKirt0zo"
DATA_FILE = "sns.json"

SN_REGEX = re.compile(r"^[A-Z0-9]{8,12}$")

# =========================
# تحميل / حفظ SN
# =========================
def load_sns():
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, "r") as f:
        return json.load(f)

def save_sns(sns):
    with open(DATA_FILE, "w") as f:
        json.dump(sns, f, indent=2)

# =========================
# Flask API
# =========================
app = Flask(__name__)

@app.route("/check_sn")
def check_sn():
    sn = request.args.get("sn", "").upper()
    if not SN_REGEX.fullmatch(sn):
        return "NO"
    sns = load_sns()
    return "OK" if sn in sns else "NO"

def run_flask():
    app.run(host="0.0.0.0", port=8080)

# =========================
# Telegram Bot
# =========================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "✅ SN Activation Bot Ready\n\n"
        "➕ Add SN:\n"
        "/addsn XXXXXXXX\n"
        "➖ Delete SN:\n"
        "/delsn XXXXXXXX\n"
        "📋 List all SNs:\n"
        "/listsn\n\n"
        "⚠️ SN must be:\n"
        "- 8 to 12 chars\n"
        "- A-Z / 0-9\n"
        "- CAPITAL only"
    )

async def addsn(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("❌ اكتب SN")
        return

    sn = context.args[0].upper()

    if not SN_REGEX.fullmatch(sn):
        await update.message.reply_text("❌ SN غير صالح")
        return

    sns = load_sns()
    if sn in sns:
        await update.message.reply_text("⚠️ SN متسجل بالفعل")
        return

    sns.append(sn)
    save_sns(sns)
    await update.message.reply_text(f"✅ SN اتفعل بنجاح:\n{sn}")

async def delsn(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("❌ اكتب SN للحذف")
        return

    sn = context.args[0].upper()
    sns = load_sns()
    if sn not in sns:
        await update.message.reply_text("⚠️ SN مش موجود")
        return

    sns.remove(sn)
    save_sns(sns)
    await update.message.reply_text(f"✅ SN اتحذف بنجاح:\n{sn}")

async def listsn(update: Update, context: ContextTypes.DEFAULT_TYPE):
    sns = load_sns()
    if not sns:
        await update.message.reply_text("⚠️ مفيش أي SN مسجلة")
        return

    message = "📋 قائمة SNs:\n" + "\n".join(sns)
    await update.message.reply_text(message)

# =========================
# تشغيل البوت
# =========================
def run_bot():
    bot_app = ApplicationBuilder().token(BOT_TOKEN).build()
    bot_app.add_handler(CommandHandler("start", start))
    bot_app.add_handler(CommandHandler("addsn", addsn))
    bot_app.add_handler(CommandHandler("delsn", delsn))
    bot_app.add_handler(CommandHandler("listsn", listsn))
    bot_app.run_polling()

# =========================
# تشغيل Flask + Telegram
# =========================
if __name__ == "__main__":
    threading.Thread(target=run_flask).start()
    run_bot()

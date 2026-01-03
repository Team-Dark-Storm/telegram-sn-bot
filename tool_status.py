from flask import Flask
import os

app = Flask(__name__)

# =========================
# التحكم في حالة التول
# =========================
TOOL_ENABLED = False  # False = يقفل البرنامج، True = يشغله

@app.route("/tool_status")
def tool_status():
    return "ENABLED" if TOOL_ENABLED else "DISABLED"

# =========================
# تشغيل السيرفر على Railway
# =========================
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))  # Railway يحدد PORT تلقائي
    app.run(host="0.0.0.0", port=port)

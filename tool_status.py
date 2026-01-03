from flask import Flask, jsonify

app = Flask(__name__)

# =========================
# إعدادات التحكم
# =========================
TOOL_ENABLED = False        # False = يقفل البرنامج
# =========================
# فحص حالة التول
# =========================
@app.route("/tool_status")
def tool_status():
    return "ENABLED" if TOOL_ENABLED else "DISABLED"




# =========================
# تشغيل السيرفر
# =========================
if __name__ == "__main__":
   port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)







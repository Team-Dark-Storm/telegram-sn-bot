from flask import Flask, jsonify

app = Flask(__name__)

# =========================
# إعدادات التحكم
# =========================
TOOL_ENABLED = True        # False = يقفل البرنامج
LATEST_VERSION = "1.0.0"  # آخر نسخة مسموحة

# =========================
# فحص حالة التول
# =========================
@app.route("/tool_status")
def tool_status():
    return "ENABLED" if TOOL_ENABLED else "DISABLED"


# =========================
# فحص التحديث
# =========================
@app.route("/check_update")
def check_update():
    return jsonify({
        "latest_version": LATEST_VERSION,
        "force_update": False
    })


# =========================
# تشغيل السيرفر
# =========================
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)

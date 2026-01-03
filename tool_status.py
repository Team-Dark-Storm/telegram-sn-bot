import os
from flask import Flask, jsonify, request

app = Flask(__name__)

# =========================
# إعدادات التحكم
# =========================
# False = يقفل البرنامج، True = مفعّل
TOOL_ENABLED = False

# =========================
# فحص حالة التول
# =========================
@app.route("/tool_status")
def tool_status():
    return "ENABLED" if TOOL_ENABLED else "DISABLED"

# =========================
# لتغيير الحالة مؤقتًا (اختياري)
# يمكن الوصول له فقط عبر POST
# =========================
@app.route("/toggle_tool", methods=["POST"])
def toggle_tool():
    global TOOL_ENABLED
    data = request.get_json() or {}
    enable = data.get("enable")
    if enable is not None:
        TOOL_ENABLED = bool(enable)
    return jsonify({"tool_enabled": TOOL_ENABLED})

# =========================
# تشغيل السيرفر
# =========================
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)

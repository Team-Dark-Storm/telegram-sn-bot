import os
from flask import Flask

app = Flask(__name__)

TOOL_ENABLED = False

@app.route("/tool_status")
def tool_status():
    return "ENABLED" if TOOL_ENABLED else "DISABLED"

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)


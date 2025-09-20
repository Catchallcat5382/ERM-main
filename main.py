from erm import run
from results import run2
import threading
from flask import Flask
import os

# -------------------------
# Flask keep-alive server
# -------------------------
app = Flask('')

@app.route('/')
def home():
    return "Bot is alive!"

def run_flask():
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)

threading.Thread(target=run_flask).start()

# -------------------------
# Run your bots
# -------------------------
if __name__ == "__main__":
    run()
    run2()  # Just call it here; __Results__ doesn't exist

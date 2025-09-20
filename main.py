from erm import run
from results import run2
from flask import Flask
import threading
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

# -------------------------
# Run Flask in a separate daemon thread
# -------------------------
flask_thread = threading.Thread(target=run_flask, daemon=True)
flask_thread.start()

# -------------------------
# Run your Discord bots in separate threads
# -------------------------
bot1_thread = threading.Thread(target=run, daemon=True)
bot2_thread = threading.Thread(target=run2, daemon=True)

bot1_thread.start()
bot2_thread.start()

# -------------------------
# Keep the main thread alive
# -------------------------
flask_thread.join()
bot1_thread.join()
bot2_thread.join()

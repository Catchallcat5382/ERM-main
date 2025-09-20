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

# Start Flask in a separate thread
threading.Thread(target=run_flask, daemon=True).start()

# -------------------------
# Run your bots in parallel
# -------------------------
if __name__ == "__main__":
    t1 = threading.Thread(target=run, daemon=True)
    t2 = threading.Thread(target=run2, daemon=True)

    t1.start()
    t2.start()

    # Keep main thread alive so Render doesn’t kill the service
    t1.join()
    t2.join()

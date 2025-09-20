from erm import run
from results import run2
from flask import Flask
import threading
import os

app = Flask('')

@app.route('/')
def home():
    return "Bot is alive!"

# Run Discord bots in threads
def run_bots():
    threading.Thread(target=run, daemon=True).start()
    threading.Thread(target=run2, daemon=True).start()

if __name__ == "__main__":
    run_bots()  # Start bots in background

    # Flask stays in main thread
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)

from flask import Flask
import os
import asyncio
import threading
from erm import run
from results import run2

app = Flask('')

@app.route('/')
def home():
    return "Bot is alive!"

def start_flask():
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)

if __name__ == "__main__":
    # Start Flask in a thread (just for Render healthcheck)
    threading.Thread(target=start_flask).start()

    # Run your Discord bots in the main thread using asyncio
    asyncio.run(run())   # Make sure run() is an async function
    asyncio.run(run2())  # Or combine them in a single async function

import os
import asyncio
from flask import Flask, request
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    ContextTypes,
    ChatMemberHandler,
)

TOKEN = os.getenv("TOKEN")
WEBHOOK_URL = os.getenv("WEBHOOK_URL")
PORT = int(os.environ.get("PORT", 8080))

if not TOKEN:
    raise ValueError("TOKEN not found")

messages = """<b>🚀 Welcome, {first}! 🚀</b>

You’ve just entered the <b>Testbook Referrer's League</b>

🔥 Daily Tips  
📊 Leaderboards  
🏆 Success Stories  
⚡ Rewards  

Let’s grow 🔥
"""

application = ApplicationBuilder().token(TOKEN).build()

async def welcome(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.chat_member:
        old = update.chat_member.old_chat_member.status
        new = update.chat_member.new_chat_member.status

        if old in ["left", "kicked"] and new in ["member", "restricted"]:
            user = update.chat_member.new_chat_member.user
            text = messages.format(first=user.first_name)

            try:
                await context.bot.send_message(
                    chat_id=user.id,
                    text=text,
                    parse_mode="HTML",
                )
            except:
                pass

application.add_handler(
    ChatMemberHandler(welcome, ChatMemberHandler.CHAT_MEMBER)
)

flask_app = Flask(__name__)

@flask_app.post("/")
async def webhook():
    update = Update.de_json(request.get_json(force=True), application.bot)
    await application.process_update(update)
    return "OK"

async def setup():
    await application.initialize()
    await application.bot.set_webhook(
        WEBHOOK_URL,
        allowed_updates=["chat_member"],
    )
    await application.start()

asyncio.get_event_loop().run_until_complete(setup())

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

if not WEBHOOK_URL:
    raise ValueError("WEBHOOK_URL not set")

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

            # ✅ Proper username detection
            if user.username:
                display_name = f"@{user.username}"
            else:
                display_name = user.mention_html()

            text = messages.format(first=display_name)

            try:
                # Try sending private message
                await context.bot.send_message(
                    chat_id=user.id,
                    text=text,
                    parse_mode="HTML",
                )
                print(f"DM sent to {display_name}")

            except Exception as e:
                print(f"DM failed: {e}")

                # Fallback message in group
                fallback_text = (
                    f"Welcome {user.mention_html()}! 🚀\n"
                    f"Click here 👉 https://t.me/{context.bot.username} "
                    f"and press Start to receive your welcome kit!"
                )

                await context.bot.send_message(
                    chat_id=update.chat_member.chat.id,
                    text=fallback_text,
                    parse_mode="HTML",
                )


application.add_handler(
    ChatMemberHandler(welcome, ChatMemberHandler.CHAT_MEMBER)
)

flask_app = Flask(__name__)

@flask_app.post("/")
async def webhook():
    update = Update.de_json(request.get_json(force=True), application.bot)
    await application.process_update(update)
    return "OK"


# ✅ Proper startup for Cloud Run
async def setup():
    await application.initialize()
    await application.bot.set_webhook(
        WEBHOOK_URL,
        allowed_updates=["chat_member"],
    )
    await application.start()

# Run async setup ONCE at container start
loop = asyncio.get_event_loop()
loop.run_until_complete(setup())

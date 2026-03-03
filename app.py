import os
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, ChatMemberHandler
from flask import Flask, request

load_dotenv()

TOKEN = os.getenv("TOKEN")
PORT = int(os.environ.get("PORT", 8080))
WEBHOOK_URL = os.getenv("WEBHOOK_URL")  # Your Cloud Run URL

if not TOKEN:
    raise ValueError("TOKEN not found in environment")

messages = """<b>🚀 Welcome, {first}! 🚀</b>
...
"""

app = ApplicationBuilder().token(TOKEN).build()

async def welcome(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.chat_member:
        old_status = update.chat_member.old_chat_member.status
        new_status = update.chat_member.new_chat_member.status

        if old_status in ["left", "kicked"] and new_status in ["member", "restricted"]:
            member = update.chat_member.new_chat_member.user
            welcome_text = messages.format(first=member.first_name)

            try:
                await context.bot.send_message(
                    chat_id=member.id,
                    text=welcome_text,
                    parse_mode="HTML"
                )
            except:
                fallback_text = f"Welcome {member.mention_html()}! 🚀 Click [here](t.me/{context.bot.username}) and press Start!"
                await context.bot.send_message(
                    chat_id=update.chat_member.chat.id,
                    text=fallback_text,
                    parse_mode="HTML"
                )

app.add_handler(ChatMemberHandler(welcome, ChatMemberHandler.CHAT_MEMBER))

flask_app = Flask(__name__)

@flask_app.post("/")
async def webhook():
    update = Update.de_json(request.get_json(force=True), app.bot)
    await app.process_update(update)
    return "OK"

if __name__ == "__main__":
    import asyncio

    async def main():
        await app.initialize()
        await app.bot.set_webhook(WEBHOOK_URL)
        await app.start()

    asyncio.run(main())
    flask_app.run(host="0.0.0.0", port=PORT)

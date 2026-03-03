from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters

TOKEN = "8618924507:AAHA-LifSUsVdZi_sFHk3R7K9uGM1oZ7Hrw"


messages = ["<b>🚀 Welcome, {first}! 🚀</b>

You’ve just entered the <b>Testbook Referrer's League</b> 

Inside this community, you’ll get:

🔥 <b>Daily Tips from Top Performers</b><br>
📊 <b>Leaderboards</b><br>
🏆 <b>Real Success Stories </b><br>
⚡ <b>Micro-Challenges & Rewards</b><br>
🎥 <b>Top Referrer Sessions</b><br>
🎁 <b>Recognition & Highlights</b><br><br>

<b>Start here, {first}:</b><br>
1️⃣ Share your current referral count<br>
2️⃣ Set your target for this week<br><br>

<b>Community Rules:</b><br>
• No hate speech<br>
• No spam links<br>
• No political/religious discussions<br>
• Referral-focused conversation only<br><br>

Top performers get featured.<br>
Consistency gets rewarded.<br><br>

Let’s see what you can do. 🔥"]

async def welcome(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.new_chat_members:
        for member in update.message.new_chat_members:
            await update.message.reply_text(
                f"🎉 Welcome {member.mention_html()} to the group! Glad to have you here!",
                parse_mode="HTML"
            )

app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(MessageHandler(filters.StatusUpdate.NEW_CHAT_MEMBERS, welcome))

print("Bot is running...")
app.run_polling()

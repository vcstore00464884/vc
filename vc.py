from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
import asyncio

BOT_TOKEN = "7620447701:AAHI49UiMBSDEo-dJku132fS4TnKl7jHeKY"
CHANNEL_ID = -1002176107287
AUTHORIZED_USER_ID = 7660776851  # 🔒 Sirf aapka Telegram User ID yahan daalein

job_ref = None
messages = []
index = 0

async def send_next(context: ContextTypes.DEFAULT_TYPE):
    global index
    if messages:
        msg = messages[index]
        await context.bot.send_message(chat_id=CHANNEL_ID, text=msg)
        index = (index + 1) % len(messages)

async def startloop(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global job_ref, messages, index

    if update.effective_user.id != AUTHORIZED_USER_ID:
        await update.message.reply_text("⛔ You're not authorized to control this bot.")
        return

    if job_ref:
        await update.message.reply_text("⚠️ Loop already running.")
        return

    if not context.args:
        await update.message.reply_text("Usage: /startloop msg1 | msg2 | msg3 ...")
        return

    full_msg = " ".join(context.args)
    messages = [msg.strip() for msg in full_msg.split("|") if msg.strip()]
    index = 0

    job_ref = context.job_queue.run_repeating(send_next, interval=5, first=0)
    await update.message.reply_text("✅ Loop started.")

async def stoploop(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global job_ref

    if update.effective_user.id != AUTHORIZED_USER_ID:
        await update.message.reply_text("⛔ You're not authorized to stop this.")
        return

    if job_ref:
        job_ref.schedule_removal()
        job_ref = None
        await update.message.reply_text("🛑 Loop stopped.")
    else:
        await update.message.reply_text("⚠️ No loop running.")

def main():
    application = Application.builder().token(BOT_TOKEN).build()
    application.add_handler(CommandHandler("startloop", startloop))
    application.add_handler(CommandHandler("stoploop", stoploop))
    application.run_polling()

if __name__ == "__main__":
    main()

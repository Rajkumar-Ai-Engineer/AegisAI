import os
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from chat_bot_agent import Chatbot
from dotenv import load_dotenv

load_dotenv()


bot = Chatbot()
bot.template()

# Get Telegram bot token
TELEGRAM_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "8451080423:AAE_E_sKh1MjOwi5vhBi8W7cTLsqFJloKks")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hi! I'm Aegis AI, your mental health assistant. How can I help you today?")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text
    
    try:
       
        response = bot.run(user_message, "en")
        await update.message.reply_text(response)
    except Exception as e:
        await update.message.reply_text(f"Sorry, I encountered an error: {str(e)}")

async def main():
    if not TELEGRAM_TOKEN:
        print("Error: TELEGRAM_BOT_TOKEN not found")
        return
    
    try:
        app = Application.builder().token(TELEGRAM_TOKEN).build()
        
        app.add_handler(CommandHandler("start", start))
        app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
        
        print("Bot is running...")
        await app.initialize()
        await app.start()
        await app.updater.start_polling()
        
        import asyncio
        await asyncio.Event().wait()
        
    except Exception as e:
        print(f"Error starting bot: {e}")

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
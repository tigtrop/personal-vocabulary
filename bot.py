from typing import Final
import os
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from googletrans import Translator
import asyncio

# Key handling - using environment variables (most secure)
TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
if not TOKEN:
    # Fallback: try to read from .env file manually
    try:
        with open('.env', 'r') as file:
            for line in file:
                if line.strip() and not line.startswith('#'):
                    key, value = line.strip().split('=', 1)
                    if key == 'TELEGRAM_BOT_TOKEN':
                        TOKEN = value
                        break
    except FileNotFoundError:
        pass
    
    if not TOKEN:
        raise ValueError(
            "TELEGRAM_BOT_TOKEN not found. Please either:\n"
            "1. Set the TELEGRAM_BOT_TOKEN environment variable, or\n"
            "2. Create a .env file with: TELEGRAM_BOT_TOKEN=your_token_here"
        )

BOT_USERNAME: Final = '@DictionaryFYbot'
user_languages = {}
translator = Translator()


# Heartbeat job
async def heartbeat_job(context: ContextTypes.DEFAULT_TYPE):
    print('Polling...')


# Commands
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message:
        return
    print(f"Received /start command from user {getattr(update.message.chat, 'id', 'unknown')}")
    keyboard = [["English", "Spanish"], ["French", "German"], ["Italian", "Ukrainian"]]
    reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True)
    await update.message.reply_text("Choose your base language:", reply_markup=reply_markup)
    if context.user_data is not None:
        context.user_data['waiting_for_language'] = True
    print(f"Sent language selection menu to user {getattr(update.message.chat, 'id', 'unknown')}")


async def set_language(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message:
        return
    user_id = getattr(update.message.chat, 'id', None)
    text = update.message.text or ''
    print(f"Received message from user {user_id}: {text}")
    waiting = context.user_data.get('waiting_for_language') if context.user_data else False
    if waiting:
        language = text.lower()
        user_languages[user_id] = language
        if context.user_data is not None:
            context.user_data['waiting_for_language'] = False
        await update.message.reply_text("Your base language is saved.")
        await update.message.reply_text("Enter word for translation:")
        print(f"User {user_id} selected language: {language}")
    else:
        await translate_message(update, context)


async def translate_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message:
        return
    user_id = getattr(update.message.chat, 'id', None)
    text = update.message.text or ''
    print(f"Processing translation for user {user_id}: {text}")
    if user_id not in user_languages:
        await update.message.reply_text("Please select a base language first by typing /start.")
        print(f"User {user_id} needs to select language first")
        return
    base_language = user_languages[user_id]
    # googletrans methods are async, so await them directly
    detected_result = await translator.detect(text)
    detected_lang = detected_result.lang
    translation_result = await translator.translate(text, src=detected_lang, dest=base_language)
    translation = translation_result.text
    await update.message.reply_text(f"Translated: {translation}")
    print(f"Translated '{text}' ({detected_lang}) to '{translation}' ({base_language}) for user {user_id}")


# Function to add jobs after app is initialized
async def post_init(application: Application):
    application.job_queue.run_repeating(heartbeat_job, interval=5, first=5)  # type: ignore


# Bot setup
if __name__ == '__main__':
    try:
        print('Starting bot...')
        print(f'Token loaded: {"Yes" if TOKEN else "No"}')
        if TOKEN:
            print(f'Token starts with: {TOKEN[:10]}...')
        
        app = Application.builder().token(TOKEN).post_init(post_init).build()

        # Commands
        app.add_handler(CommandHandler('start', start_command))

        # Language selection
        app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, set_language))

        print('Bot started successfully!')
        print('Bot username:', BOT_USERNAME)
        print('Bot is now listening for messages...')
        print('Press Ctrl+C to stop the bot')
        print('Polling...')
        app.run_polling(poll_interval=5)
    except Exception as e:
        print(f'Error starting bot: {e}')
        import traceback
        traceback.print_exc()
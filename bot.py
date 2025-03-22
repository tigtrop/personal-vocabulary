from typing import Final
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from googletrans import Translator

# Key handling
file_path = "C:/DictionaryBOT/keys/key.txt"
try:
    with open(file_path, 'r') as file:
        key = file.read().strip()
    print("Key successfully loaded!")
except FileNotFoundError:
    print(f"File not found: {file_path}")
except Exception as e:
    print(f"An error occurred: {e}")

TOKEN: Final = key
BOT_USERNAME: Final = '@DictionaryFYbot'
user_languages = {}
translator = Translator()


# Commands
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [["English", "Spanish"], ["French", "German"], ["Italian", "Ukrainian"]]
    reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True)
    await update.message.reply_text("Choose your base language:", reply_markup=reply_markup)
    context.user_data['waiting_for_language'] = True


async def set_language(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.chat.id
    if 'waiting_for_language' in context.user_data and context.user_data['waiting_for_language']:
        language = update.message.text.lower()
        user_languages[user_id] = language
        context.user_data['waiting_for_language'] = False
        await update.message.reply_text("Your base language is saved.")
        await update.message.reply_text("Enter word for translation:")
    else:
        await translate_message(update, context)


async def translate_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.chat.id
    text = update.message.text

    if user_id not in user_languages:
        await update.message.reply_text("Please select a base language first by typing /start.")
        return

    base_language = user_languages[user_id]
    detected_lang = (await translator.detect(text)).lang
    translation = (await translator.translate(text, src=detected_lang, dest=base_language)).text

    await update.message.reply_text(f"Translated: {translation}")


# Bot setup
if __name__ == '__main__':
    print('Starting bot...')
    app = Application.builder().token(TOKEN).build()

    # Commands
    app.add_handler(CommandHandler('start', start_command))

    # Language selection
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, set_language))

    print('Polling...')
    app.run_polling(poll_interval=5)
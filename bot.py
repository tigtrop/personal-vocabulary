from typing import Final
from telegram import Update
from telegram.ext import  Application, CommandHandler, MessageHandler,filters, ContextTypes

# Key handling

file_path = "C:/DictionaryBOT/keys/key.txt"

try:
    with open(file_path, 'r') as file:
        key = file.read()  # Read the content of the file into the key variable
    print("Key successfully loaded!")
except FileNotFoundError:
    print(f"File not found: {file_path}")
except Exception as e:
    print(f"An error occurred: {e}")

TOKEN: Final = key
BOT_USERNAME: Final = '@DictionaryFYbot'

# Commands
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Hello! I will save and translate some words for you.')

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Just put a word')

# Respondes

def handle_response(text: str) -> str:
    proccesed: str = text.lower()

    if 'Hello' in text:
        return 'You hello'

    return 'Try again.'

async  def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message_type: str = update.message.chat.type
    text: str = update.message.text

    print(f'User ({update.message.chat.id}) in {message_type}: "{text}"')

    if message_type == 'group':
        if BOT_USERNAME in text:
            new_text: str = text.replace(BOT_USERNAME, '').strip()
            response: str = handle_response(new_text)
        else:
            return

    else:
        response: str = handle_response(text)

    print('Bot:', response)
    await  update.message.reply_text(response)

async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f'Update {update} caused error {context.error}')

if __name__ == '__main__':
    print('Starting bot...')
    app = Application.builder().token(TOKEN).build()

    # Commands
    app.add_handler(CommandHandler('start', start_command))

    # Messages

    app.add_handler(MessageHandler(filters.TEXT, handle_message))

    # Errors

    app.add_error_handler(error)

    # Polls the bot

    print('Polling...')
    app.run_polling(poll_interval=5)













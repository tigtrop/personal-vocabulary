# Personal Vocabulary Bot

A Telegram bot for translating words and building personal vocabulary.

## Setup

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Set up your Telegram Bot Token:**
   
   **Option A: Using .env file (recommended for development)**
   - Copy `env.example` to `.env`
   - Edit `.env` and replace `your_telegram_bot_token_here` with your actual bot token
   
   **Option B: Using environment variable**
   - Set the environment variable: `TELEGRAM_BOT_TOKEN=your_actual_token`
   
   **Option C: Using system environment variable**
   - Windows: `set TELEGRAM_BOT_TOKEN=your_actual_token`
   - Linux/Mac: `export TELEGRAM_BOT_TOKEN=your_actual_token`

3. **Run the bot:**
   ```bash
   python bot.py
   ```

## Getting a Telegram Bot Token

1. Message [@BotFather](https://t.me/botfather) on Telegram
2. Send `/newbot` and follow the instructions
3. Copy the token provided by BotFather

## Security Notes

- Never commit your `.env` file or any files containing your bot token
- The `.gitignore` file is configured to exclude sensitive files
- Use environment variables in production environments

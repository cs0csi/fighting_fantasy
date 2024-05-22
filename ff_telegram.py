import configparser
import os
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# Configuration file path
config_file_path = 'telegram_config.ini'

if not os.path.exists(config_file_path):
    raise FileNotFoundError(f"The configuration file {
                            config_file_path} does not exist.")

config = configparser.ConfigParser()
config.read(config_file_path)

if 'settings' in config:
    TOKEN = config['settings'].get('token')
    BOT_USERNAME = config['settings'].get('bot_username')
    print(f"TOKEN: {TOKEN}, BOT_USERNAME: {BOT_USERNAME}")
else:
    raise KeyError(
        "The 'settings' section is missing in the configuration file.")

# Define the bot commands and handlers


async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Hello I am banana')


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Type something and I can respond')


async def custom_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('this is custom')


def handle_response(text: str) -> str:
    processed = text.lower()

    if 'hello' in processed:
        return 'Hello, how are you today?'
    elif 'bye' in processed:
        return 'Goodbye! Have a great day.'
    else:
        return 'I didnt understand that.'


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message_type: str = update.message.chat.type
    text: str = update.message.text

    print(f' User ({update.message.chat.id}) in {message_type}: "{text}"')

    if message_type == 'group':
        if BOT_USERNAME in text:
            new_text: str = text.replace(BOT_USERNAME, '').strip()
            response: str = handle_response(new_text)
        else:
            return
    else:
        response: str = handle_response(text)

    print('Bot:', response)
    await update.message.reply_text(response)


async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f'update {Update} caused error {context.error}')

if __name__ == '__main__':
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler('start', start_command))
    app.add_handler(CommandHandler('help', help_command))
    app.add_handler(CommandHandler('custom', custom_command))

    app.add_handler(MessageHandler(filters.TEXT, handle_message))

    app.add_error_handler(error)

    print('polling...')

    app.run_polling(poll_interval=3)

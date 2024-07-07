import configparser
import os
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

import random
import sys

# Try importing stories
try:
    from stories import stories
except ModuleNotFoundError as e:
    print(f"Error: {e}")
    sys.exit(
        "Required module 'stories' not found. Please ensure it is installed and accessible.")

# Try importing enemies
try:
    from enemies import enemies
except ModuleNotFoundError as e:
    print(f"Error: {e}")
    sys.exit(
        "Required module 'enemies' not found. Please ensure it is installed and accessible.")

from player_inventory import inventory, fuel_level, car_inventory, show_inventory
from character_create import create_character
from car_create import create_car
from inventory.inventory import check_car_inventory, modify_inventory, check_inventory, show_inventory
from combat.combat import start_car_combat, start_firearms_combat, start_close_combat, duel, car_race
from game_logic.game_logic import modify_prop, select_enemies, test_of_dexterity, test_of_luck_without_minus, test_of_luck, check_hp, d6, test_of_dexterity_different, dex_compare
import os


# Configuration file path
config_file_path = 'telegram_config.ini'

# Checking if the configuration file exists
if not os.path.exists(config_file_path):
    raise FileNotFoundError(f"The configuration file {
                            config_file_path} does not exist.")

# Reading configuration from the file
config = configparser.ConfigParser()
config.read(config_file_path)

# Retrieving bot settings from the configuration
if 'settings' in config:
    TOKEN = config['settings'].get('token')
    BOT_USERNAME = config['settings'].get('bot_username')
    print(f"TOKEN: {TOKEN}, BOT_USERNAME: {BOT_USERNAME}")
else:
    raise KeyError(
        "The 'settings' section is missing in the configuration file.")


async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE, parameter_text: str) -> None:
    """Echo the user message."""
    await update.message.reply_text(parameter_text)

await echo(update, context, "This is the parameter text")

# Define the bot commands and handlers
current_story_key = "2"
current_story = stories[current_story_key]
current_story_text = current_story["text"]
# Handler for /start command


async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Hello I am banana')

# Handler for /help command


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Type something and I can respond')

# Handler for a custom command


async def custom_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('this is custom')

# Function to handle responses based on user input


def handle_response(text: str) -> str:
    processed = text.lower()
# IF you paste here something the function will crash with: update <class 'telegram._update.Update'> caused error 2
    if 'hi' in processed:
        return current_story_text
    elif 'bye' in processed:
        return 'Goodbye! Have a great day.'
    else:
        return 'I didn\'t understand that.'

# Handler for incoming messages


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message_type: str = update.message.chat.type
    text: str = update.message.text

    # Logging user messages
    print(f' User ({update.message.chat.id}) in {message_type}: "{text}"')

    # Handling messages differently based on the chat type
    if message_type == 'group':
        if BOT_USERNAME in text:
            new_text: str = text.replace(BOT_USERNAME, '').strip()
            response: str = handle_response(new_text)
        else:
            return
    else:
        response: str = handle_response(text)

    # Sending the bot's response
    print('Bot:', response)
    await update.message.reply_text(response)

# Handler for errors


async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f'update {Update} caused error {context.error}')

# Main program
if __name__ == '__main__':
    # Creating the Telegram bot application
    app = Application.builder().token(TOKEN).build()

    # Adding command handlers
   # app.add_handler(CommandHandler('start', start))
    app.add_handler(CommandHandler('help', help_command))
    app.add_handler(CommandHandler('custom', custom_command))

   async def echo_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
        await echo(update, context, "This is the parameter text")

    # Add the handler to the application
    echo_handler = CommandHandler('echo', echo_command)
    app.add_handler(echo_handler)

    # Adding message handler
    app.add_handler(MessageHandler(filters.TEXT, handle_message))

    # Adding error handler
    app.add_error_handler(error)

    # Starting the bot and polling for updates
    print('polling...')
    app.run_polling(poll_interval=3)

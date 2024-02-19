import logging
from telegram import Update, Bot
from telegram.ext import Updater, CommandHandler, CallbackContext
from apscheduler.schedulers.background import BackgroundScheduler
import pytz
import requests
from random import choice
import os
import urllib3

# Bot Token
TOKEN = '7078028281:AAGPuTi-8fiHrkvacxD-EfmpbG6b0YJebYs'
bot = Bot(token=TOKEN)

# Logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# GitHub Flashcards URL
GITHUB_REPO_URL = 'https://github.com/4rchB1sh0p/german_flashcards_telegram_bot/blob/main/flashcards/'
GITHUB_RAW_URL = 'https://raw.githubusercontent.com/4rchB1sh0p/german_flashcards_telegram_bot/main/flashcards/'

def generate_flashcard_names():
    """
    Generate a list of flashcard filenames based on the naming convention.
    The list will include both .jpg and .png files from name_001 to name_300.
    """
    flashcard_names = []
    for i in range(1, 301):  # Generates numbers from 1 to 300
        number_str = f'{i:03}'  # Formats the number as a three-digit string (001, 002, ..., 300)
        # Add both .jpg and .png filenames for each number
        flashcard_names.append(f'name_{number_str}.jpg')
        flashcard_names.append(f'name_{number_str}.png')
    return flashcard_names

# Now use this function to fetch a random flashcard
def fetch_random_flashcard():
    """
    Fetch a random flashcard URL from dynamically generated names,
    supporting both .jpg and .png files.
    """
    flashcard_names = generate_flashcard_names()  # Generate the list of flashcard names
    selected_flashcard = choice(flashcard_names)  # Randomly select a flashcard
    flashcard_url = f'https://raw.githubusercontent.com/4rchB1sh0p/german_flashcards_telegram_bot/main/flashcards/{selected_flashcard}'
    return flashcard_url


def send_flashcard(update: Update, context: CallbackContext):
    """
    Send a random flashcard to the chat.
    """
    flashcard_url = fetch_random_flashcard()
    chat_id = update.message.chat_id
    bot.send_photo(chat_id=chat_id, photo=flashcard_url)

def daily_flashcard(context: CallbackContext):
    """
    Callback function for sending daily flashcard.
    """
    job = context.job
    flashcard_url = fetch_random_flashcard()
    bot.send_photo(chat_id=job.context, photo=flashcard_url)

def start(update: Update, context: CallbackContext):
    """
    Start command to schedule daily flashcards.
    """
    chat_id = update.message.chat_id
    # Schedule daily flashcard at 1 PM IST
    scheduler = BackgroundScheduler()
    scheduler.configure(timezone=pytz.timezone('Asia/Kolkata'))
    scheduler.add_job(daily_flashcard, 'cron', hour=13, minute=0, context=chat_id)
    scheduler.start()
    update.message.reply_text('Scheduled daily flashcards at 1 PM IST.')

def flash_me(update: Update, context: CallbackContext):
    """
    Command to immediately send a flashcard.
    """
    send_flashcard(update, context)

def main():
    """
    Main function to start the bot.
    """
    #updater = Updater(TOKEN)
    updater = Updater(token=TOKEN,use_context=True)
    dp = updater.dispatcher

    # Command Handlers
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("flash_me", flash_me))

    # Start the Bot
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()

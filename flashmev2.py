import logging
from telegram import Update, Bot
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackContext, ContextTypes
from apscheduler.schedulers.background import BackgroundScheduler
import pytz
import requests
from random import choice
import os
import urllib3

# Bot Token
TOKEN = "TOKEN"
bot = Bot(token=TOKEN)

#venv setup commandds
#venv\scripts\activate
#Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process
#pip install python-telegram-bot --upgrade

# Logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# GitHub Flashcards URL
GITHUB_REPO_URL = 'https://github.com/4rchB1sh0p/german_flashcards_telegram_bot/blob/main/flashcards/'
GITHUB_RAW_URL = 'https://raw.githubusercontent.com/4rchB1sh0p/german_flashcards_telegram_bot/main/flashcards/'

def generate_flashcard_names():
    """
    Generate a list of flashcard filenames based on the naming convention.
    The list will include both .jpg and .png files from name_001 to name_300.
    """
    flashcard_names = []
    for i in range(1, 200):  # Generates numbers from 1 to 200
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


""" def send_flashcard(update: Update, context: CallbackContext):
    
    flashcard_url2 = fetch_random_flashcard()
    chat_id = update.message.chat_id
    bot.send_photo(chat_id=chat_id, photo=flashcard_url2) """

async def daily_flashcard(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Callback function for sending daily flashcard.
    """
    #job = context.job
    flashcard_url = fetch_random_flashcard()
    await context.bot.send_photo(chat_id=update.effective_chat.id,photo=flashcard_url)
    #bot.send_photo(chat_id=job.context, photo=flashcard_url)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Start command to schedule daily flashcards.
    """
    # Schedule daily flashcard at 1 PM IST
    #scheduler = BackgroundScheduler()
    #scheduler.configure(timezone=pytz.timezone('Asia/Kolkata'))
    #scheduler.add_job(daily_flashcard, 'cron', hour=13, minute=0,context=update.effective_chat.id)
    #scheduler.start() 
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Scheduled daily flashcards at 1 PM IST.")

""" def start2(update: Update, context: CallbackContext):
  
    Start command to schedule daily flashcards.

    chat_id = update.message.chat_id
    # Schedule daily flashcard at 1 PM IST
    scheduler = BackgroundScheduler()
    scheduler.configure(timezone=pytz.timezone('Asia/Kolkata'))
    scheduler.add_job(daily_flashcard, 'cron', hour=13, minute=0, context=chat_id)
    scheduler.start()
    update.message.reply_text('Scheduled daily flashcards at 1 PM IST.') """

async def flash_me(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Command to immediately send a flashcard.
    """
    flashcard_url = fetch_random_flashcard()
    #await context.bot.send_message(chat_id=update.effective_chat.id, text=flashcard_url)
    await context.bot.send_photo(chat_id=update.effective_chat.id,photo=flashcard_url)
    #send_flashcard(update, context)

def main():
    """
    Main function to start the bot.
    """
    #updater = Updater(TOKEN)
    #updater = Updater(token=TOKEN,use_context=True)
    dp = ApplicationBuilder().token(TOKEN).build()


    # Command Handlers
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("flash_me", flash_me))

    # Start the Bot
    dp.run_polling()
    #updater.start_polling()
    #updater.idle()

if __name__ == '__main__':
    main()

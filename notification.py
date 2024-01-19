import telegram
import schedule
from telegram import Update
import time
# from telegram import Bot as bot

from datetime import datetime
from threading import Thread
from telegram.ext import Updater, CommandHandler, CallbackContext

# Replace 'YOUR_BOT_TOKEN' with the actual bot token you obtained from BotFather
BOT_TOKEN = '6709665712:AAE1c4WP68WJ4UzJsoGWPJlAmyYvmC9GnlE'
# Create a bot instance
chat_id = ['1434469177', '314924178', ]
bot = telegram.Bot(token=BOT_TOKEN)

# Dictionary to store user chat IDs
user_chat_ids = {}

def start(update: Update, context: CallbackContext):
    user_id = update.effective_user.id
    context.bot.send_message(chat_id=user_id, text="Welcome to the Card Birr Bot!")
    context.bot.send_message(chat_id=user_id, text="Your chat ID is: {}".format(user_id))
    user_chat_ids[user_id] = user_id  # Store the chat ID for future use
    
    
def send_notification(bot, user_id, message):
    """Send a notification to a specific user."""
    bot.send_message(user_id, text=message)

def send_notifications_to_all_users(updater: Updater, message:str):
    """Send a notification to all users who have interacted with the bot."""
    bot = updater.bot
    print("kkkkkkkkkkkkkkkkkkk", bot, message )

    # all_users = get_all_users_from_database()
    print("hjjjjjjjjj",bot)  

    # Send the message to each user
    for user_id in chat_id:
        send_notification(bot, user_id, message)  
        print("hjjjjjjjjj",bot, user_id)  

# def send_notification(user_id):
#     message = "Hello user, this is your Tuesday notification at 15:20. Please use our service."
#     bot.send_message(chat_id=user_id, text=message)

# def get_chat_id():
    
#     current_time = datetime.now().strftime("%H:%M")
#     current_day = datetime.now().strftime("%A")

#     if current_day.lower() == 'wednesday' and current_time == "04:34":
#       for user_id in user_chat_ids.values():
        
#         send_notification(user_id)

# def scheduler_thread():
#     while True:
#         schedule.run_pending()
#         time.sleep(1)

# # Schedule the get_chat_id function every minute
# schedule.every(1).minutes.do(get_chat_id)

# Schedule the get_chat_id function for Monday at 11:00
# schedule.every().wednesday.at("04:13").do(get_chat_id)

def main():
    updater = Updater(token=BOT_TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler('start', start))

    # print('Starting scheduler thread...')
    # scheduler = Thread(target=scheduler_thread)
    # scheduler.start()

    print('Polling...')
    updater.start_polling()
     # Send notifications to all users when the script is run
    send_notifications_to_all_users(updater, "This is a notification from your bot!")

    
    updater.idle()

if __name__ == "__main__":
    main()

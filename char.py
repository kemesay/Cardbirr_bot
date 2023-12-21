from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler

# Define your callback function to handle the button press
def button_callback(update, context):
    query = update.callback_query
    query.answer()
    query.edit_message_text(text=f"Button pressed! Callback data: {query.data}")

# Define the function to start the bot and set up the menu
def start(update, context):
    keyboard = [
        [InlineKeyboardButton("Press me", callback_data='press_button')],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text('Welcome to the bot!', reply_markup=reply_markup)

# Set up the main function
def main():
    # Set up the Telegram Bot with your token
    updater = Updater(token='6709665712:AAE1c4WP68WJ4UzJsoGWPJlAmyYvmC9GnlE', use_context=True)
    dp = updater.dispatcher

    # Add a handler to respond to the /start command
    dp.add_handler(CommandHandler("start", start))

    # Add a CallbackQueryHandler to handle button presses
    dp.add_handler(CallbackQueryHandler(button_callback))

    # Start the bot
    updater.start_polling()
    updater.idle()

# Run the bot
if __name__ == '__main__':
    main()

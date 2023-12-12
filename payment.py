from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler, CallbackQueryHandler, CallbackContext

# Define states for the first conversation
FIRST, SECOND = range(2)

# Define states for the second conversation (phone number)
PHONE_NUMBER = range(1)

# Function to start the first conversation
def start(update: Update, context: CallbackContext) -> int:
    keyboard = [[InlineKeyboardButton("Start First Conversation", callback_data='start_first')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text("Hi! Choose an option:", reply_markup=reply_markup)
    return FIRST

# Function for the first step in the first conversation
def first_step(update: Update, context: CallbackContext) -> int:
    update.message.reply_text("This is the first step. What's next?")
    return SECOND

# Function for the second step in the first conversation
def second_step(update: Update, context: CallbackContext) -> int:
    update.message.reply_text("This is the second step. First conversation completed.")
    return ConversationHandler.END

# Function to cancel the first conversation
def cancel(update: Update, context: CallbackContext) -> int:
    update.message.reply_text("First conversation cancelled.")
    return ConversationHandler.END

# Create the first ConversationHandler with states and corresponding functions
first_conv_handler = ConversationHandler(
    entry_points=[CommandHandler('start', start)],

    states={
        FIRST: [MessageHandler(Filters.text & ~Filters.command, first_step)],
        SECOND: [MessageHandler(Filters.text & ~Filters.command, second_step)],
    },

    fallbacks=[CommandHandler('cancel', cancel)]
)

# Function to start the second conversation (phone number)
def start_phone_number(update: Update, context: CallbackContext) -> int:
    update.message.reply_text("Please send me your phone number.")
    return PHONE_NUMBER

# Function to handle the phone number input
def phone_number_handler(update: Update, context: CallbackContext) -> int:
    phone_number = update.message.text
    update.message.reply_text(f"Phone number received: {phone_number}")
    return ConversationHandler.END

# Function to handle the inline keyboard button click
def inline_button_callback(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    query.answer()
    
    if query.data == 'start_first':
        return start_phone_number(update, context)

# Create the second ConversationHandler for phone number input
phone_number_conv_handler = ConversationHandler(
    entry_points=[CallbackQueryHandler(inline_button_callback)],

    states={
        PHONE_NUMBER: [MessageHandler(Filters.text & ~Filters.command, phone_number_handler)],
    },

    fallbacks=[CommandHandler('cancel', cancel)]
)

# Set up the bot with both ConversationHandlers
updater = Updater("6680224136:AAH95LjUiyLSC8PuyMy10jXxx4-op2i-teI", use_context=True)
dp = updater.dispatcher
dp.add_handler(first_conv_handler)
dp.add_handler(phone_number_conv_handler)

# Start the bot
updater.start_polling()
updater.idle()

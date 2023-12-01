from telegram import KeyboardButton, ReplyKeyboardMarkup
from telegram.ext import Updater, MessageHandler, Filters, CallbackContext, CommandHandler

def get_keyboard():
    contact_button = KeyboardButton('Agree to share your phone Number', request_contact=True)
    reply_keyboard = [[contact_button]]
    return ReplyKeyboardMarkup(reply_keyboard, resize_keyboard=True)

def contact_callback(update, context: CallbackContext):
    contact = update.effective_message.contact
    phone = contact.phone_number
    print(f"Contact received: {contact}")
    print(f"Phone number: {phone}")
    update.message.reply_text('Thanks, your data is accepted.', reply_markup=get_keyboard())

def start(update, context: CallbackContext):
    update.message.reply_text('Welcome! To start a conversation, please share your contact information.', reply_markup=get_keyboard())

def main():
    updater = Updater(token="6796089767:AAGMhYGI9KCV2MEuFSNy3_T10DFiSHDvJGM", use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler('start', start))
    dp.add_handler(MessageHandler(Filters.contact, contact_callback, pass_user_data=True))

    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()

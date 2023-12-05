from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, MessageHandler, Filters, ConversationHandler, CallbackContext

# Constants
PHONE_NUMBER = range(1)

# Global variables
PHONE = ""
CONTACT_INFO_PROCESSED = False
cardValue = ""
Safaricom = ""
EthioTelecom = ""
cardType = ""

# Conversation states
GET_PHONE_NUMBER = 0

def start(update: Update, context: CallbackContext):
    context.bot.send_message(chat_id=update.effective_user.id,
                             text=f"Hello Mr/Mrs. {update.effective_user.first_name} \n Welcome to the Card Birr Bot!",
                             reply_markup=get_keyboard())

def handle_button_click(update: Update, context: CallbackContext):
    global cardValue, cardType
    query = update.callback_query
    query.answer()
    payload = query.data

    if payload in list_button_click:
        cardValue = payload
        context.bot.send_message(chat_id=update.effective_user.id, text=f"You have selected {cardValue} Birr")
        context.bot.send_message(chat_id=update.effective_user.id,
                                 text="Please enter the phone number you want to charge")

        # Set the conversation state to GET_PHONE_NUMBER
        return GET_PHONE_NUMBER

    elif query.data == "Balance":
        context.bot.send_message(chat_id=update.effective_user.id, text=f"Mr/Mrs. {update.effective_user.first_name}")
    elif query.data == "transfertowallet":
        context.bot.send_message(chat_id=update.effective_user.id, text=f"Mr/Mrs. {update.effective_user.first_name}")

    return ConversationHandler.END

def get_phone_number(update: Update, context: CallbackContext):
    global cardType

    # Retrieve the phone number from user input
    phone_number = update.message.text

    # You can further process the phone number or use it as needed
    context.bot.send_message(chat_id=update.effective_user.id, text=f"Phone number: {phone_number}")

    # Call the message_handler function to handle the message
    cardType = message_handler(update, context)

    # End the conversation
    return ConversationHandler.END

def message_handler(update: Update, context: CallbackContext):
    global EthioTelecom, Safaricom
    text = update.message.text

    if text == "Ethio telecom Top Ups":
        ethio_telecom_key = [[InlineKeyboardButton(text="5 Birr", callback_data="5"),
                              InlineKeyboardButton(text="10 Birr", callback_data="10"),
                              InlineKeyboardButton(text="15 Birr", callback_data="15"),
                              ],
                             [
                                 InlineKeyboardButton(text="20 Birr", callback_data="20"),
                                 InlineKeyboardButton(text="25 Birr", callback_data="25"),
                                 InlineKeyboardButton(text="50 Birr", callback_data="50"),
                             ],
                             [
                                 InlineKeyboardButton(text="100 Birr", callback_data="100"),
                                 InlineKeyboardButton(text="500 Birr", callback_data="500"),
                                 InlineKeyboardButton(text="1000 Birr", callback_data="1000")
                             ]
                             ]
        reply_markup = InlineKeyboardMarkup(ethio_telecom_key)
        update.message.reply_text("You can select the card amount you want to fill", reply_markup=reply_markup)
        return EthioTelecom
    elif text == "Safari com Top Ups":
        safaricom_key = [[InlineKeyboardButton(text="5 Birr", callback_data="5"),
                          InlineKeyboardButton(text="10 Birr", callback_data="10"),
                          InlineKeyboardButton(text="15 Birr", callback_data="15"),
                          ],
                         [
                             InlineKeyboardButton(text="20 Birr", callback_data="20"),
                             InlineKeyboardButton(text="25 Birr", callback_data="25"),
                             InlineKeyboardButton(text="50 Birr", callback_data="50"),
                         ],
                         [
                             InlineKeyboardButton(text="100 Birr", callback_data="100"),
                             InlineKeyboardButton(text="500 Birr", callback_data="500"),
                             InlineKeyboardButton(text="1000 Birr", callback_data="100")
                         ]
                         ]
        reply_markup = InlineKeyboardMarkup(safaricom_key)
        update.message.reply_text("You can select the card amount you want to fill", reply_markup=reply_markup)
        return Safaricom
    elif text == "Account":
        update.message.reply_text(text="You can check the amount or transfer your balance from Banks to this wallet",
                                  reply_markup=account_menu())
    elif text == "Help":
        update.message.reply_text(text="Coming Soon")

    return ConversationHandler.END

def main():
    updater = Updater(token="YOUR_TOKEN", use_context=True)
    dp = updater.dispatcher

    # Create a ConversationHandler with states
    conv_handler = ConversationHandler(
        entry_points=[CallbackQueryHandler(handle_button_click)],
        states={
            GET_PHONE_NUMBER: [MessageHandler(Filters.text, get_phone_number)],
        },
        fallbacks=[],
    )

    dp.add_handler(conv_handler)
    dp.add_handler(CommandHandler('start', start))
    dp.add_handler(MessageHandler(Filters.contact, contact_callback, pass_user_data=True))
    dp.add_handler(MessageHandler(Filters.location | Filters.text, message_handler, pass_chat_data=True))

    print('Polling...')
    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()

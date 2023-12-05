from telegram import InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, Location, ReplyKeyboardMarkup, Update, InputMediaPhoto
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, CallbackContext, Updater, CommandHandler, MessageHandler, \
    Filters, ConversationHandler, CallbackQueryHandler

import re
import requests
import json

PHONE_NUMBER = range(1)
cardValue = ""
cardType = ""
phoneNumber = ""
dict_user = {}
count = 0.0

def spinning_win_button():
    btn = [[InlineKeyboardButton(text="Play Spinning", callback_data="Playsw")]]
    return InlineKeyboardMarkup(btn)


def depo_button():
    btn = [[InlineKeyboardButton(text="Deposit", callback_data="transfer")]]
    return InlineKeyboardMarkup(btn)


def user_register():
    btn = [[InlineKeyboardButton(text="Register yourself", callback_data="registration")]]
    return InlineKeyboardMarkup(btn)


def main_menu():
    main_keyboard = [
        [KeyboardButton(text="Ethio telecom Top Ups"), KeyboardButton(text="Safari com Top Ups")],
        [KeyboardButton(text="Account"), KeyboardButton(text="Help")]
    ]
    return ReplyKeyboardMarkup(main_keyboard)


def account_menu():
    main_keyboard = [
        [InlineKeyboardButton(text="Check your Balance", callback_data="Balance"),
         InlineKeyboardButton(text="Transfer Banks to Wallet", callback_data="transfertowallet")],
    ]
    return InlineKeyboardMarkup(main_keyboard)


def recharge_menu():
    main_keyboard = [
        [InlineKeyboardButton(text="This phone", callback_data="thisphone"),
         InlineKeyboardButton(text="Other phone", callback_data="otherphone")],
    ]
    return InlineKeyboardMarkup(main_keyboard)


def get_keyboard():
    reply_keyboard = [[KeyboardButton(text='Are you agree to share your Phone Number', request_contact=True, id=1)]]
    return ReplyKeyboardMarkup(reply_keyboard, resize_keyboard=True, one_time_keyboard=True)


def message_overtaken(update, context):
    global cardValue, cardType, phoneNumber
    users = update.message.from_user
    print(users, "dffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff")
    if update.message.text in ['Ethio telecom Top Ups', 'Safari com Top Ups']:
        phoneNumber = str(update.message.text)
        print('tyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyy')
        if re.match(r'^\d{10}$', phoneNumber):
            context.user_data['phoneNumber'] = phoneNumber
            cardType = select_card_type(update, context)
            cardValue = select_card_value(update, context)

            api_url = "https://cardapi.zowibot.com/api/v1/cards/recharge"
            data = {
                "cardValue": cardValue,
                "cardType": cardType,
                "phoneNumber": phoneNumber
            }

            headers = {
                'Content-Type': 'application/json',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                              'Chrome/117.0.0.0 Safari/537.36',
                'telegram_user_id': str(update.effective_user.id)
            }

            try:
                response = requests.post(api_url, json=data, headers=headers)
                err = response.text
                response.raise_for_status()
                print(headers, data)
                if response.status_code == 200:
                    context.bot.send_message(
                        chat_id=update.effective_user.id,
                        text="The phone is successfully charged!"
                    )
                    return ConversationHandler.END

                elif response.status_code == 400 or response.status_code == 404:
                    context.bot.send_message(
                        chat_id=update.effective_user.id,
                        text=f"{json.loads(err).get('message')}")
                    return ConversationHandler.END

            except requests.exceptions.RequestException as e:
                context.bot.send_message(
                    chat_id=update.effective_user.id,
                    text=f"{json.loads(err).get('message')}")
                return ConversationHandler.END

        else:
            update.message.reply_text("Invalid phone number format. Please enter a 10-digit phone number.")
            return ConversationHandler.END


def contact_callback(update, context):
    if update.message.contact:
        phone_number = update.message.contact.phone_number
        telegram_user_id = str(update.effective_user.id)
        first_name = update.effective_user.first_name

        api_url = "https://cardapi.zowibot.com/api/v1/users"
        data = {
            'phoneNumber': phone_number,
            'telegramUserId': telegram_user_id,
            'firstName': first_name,
        }

        headers = {
            'Content-Type': 'application/json',
        }

        try:
            response = requests.post(api_url, json=data, headers=headers)

            if response.status_code == 201:
                context.bot.send_message(chat_id=update.effective_user.id,
                                         text="Select the service you want!",
                                         reply_markup=main_menu())
        except requests.exceptions.RequestException as e:
            print(f"Error submitting phone number: {e}")
    else:
        print("No contact information received.")


def start(update, context):
    context.bot.send_message(chat_id=update.effective_user.id,
                             text=f"Hello Mr/Mrs. {update.effective_user.first_name} \n Welcome to the Card Birr Bot!",
                             reply_markup=get_keyboard())


list_button_click = ["5", "10", "15", "20", "25", "50", "100", "500", "1000"]


def select_card_type(update, context):
    text = update.message.text
    if text == "Ethio telecom Top Ups":
        return 'Ethio_Telecom'
    elif text == "Safari com Top Ups":
        return 'Safaricom'


def select_card_value(update, context):
    query = update.callback_query
    query.answer()
    payload = query.data
    if payload in list_button_click:
        return payload


def handle_button_click(update, context):
    global cardValue, cardType
    cardValue = select_card_value(update, context)
    query = update.callback_query
    query.answer()
    payload = query.data
    if payload in list_button_click:
        cardValue = payload
        context.bot.send_message(chat_id=update.effective_user.id,
                                 text=f"You have selected {cardValue} Birr from {cardType}")
        context.bot.send_message(chat_id=update.effective_user.id,
                                 text="Please enter the phone number you want to charge")
        print(cardType, cardValue)
        return PHONE_NUMBER
    elif payload == "Balance":
        telegram_user_id = str(update.effective_user.id)
        api_url = "https://cardapi.zowibot.com/api/v1/users/me"

        headers = {
            'Content-Type': 'application/json',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/117.0.0.0 Safari/537.36',
            'telegram_user_id': telegram_user_id
        }

        try:
            response = requests.get(api_url, headers=headers)
            if response.status_code == 200:
                response = response.json()
                balance = response['Wallet']['balance']
                currency = response['Wallet']['currency']
                context.bot.send_message(chat_id=update.effective_user.id,
                                         text=f"Hello {update.effective_user.first_name} your current balance is  {balance} {currency}")
            else:
                context.bot.send_message(chat_id=update.effective_user.id,
                                         text=f"Sorry {update.effective_user.first_name} try again later!")

        except requests.exceptions.RequestException as e:
            print(f"Error submitting phone number: {e}")

    elif payload == "transfertowallet":
        context.bot.send_message(chat_id=update.effective_user.id,
                                 text=f"Mr/Mrs. {update.effective_user.first_name}")


def message_handler(update, context):
    global cardType, cardValue
    cardType = select_card_type(update, context)
    # cardValue = select_card_value(update, context)

    text = update.message.text
    if text == "Ethio telecom Top Ups" or text == "Safari com Top Ups":
        keyboard = create_recharge_keyboard(text)
        update.message.reply_text(f"You can select the card amount you want to fill for {cardType}" , reply_markup=keyboard)
        
        return ConversationHandler.END
    
    elif text=='Ethio telecom Top Ups' or 'Safari com Top Ups' and  count == 0:
        return message_overtaken(update, context)
    
    elif text == "Account":
        update.message.reply_text(text="You can check Amount or Transfer your balance from Banks to this wallet",
                                  reply_markup=account_menu())
    elif text == "Help":
        update.message.reply_text(text="Coming Soon")


def create_recharge_keyboard(operator):
    recharge_key = [
        [InlineKeyboardButton(text="5 Birr", callback_data="5"),
         InlineKeyboardButton(text="10 Birr", callback_data="10"),
         InlineKeyboardButton(text="15 Birr", callback_data="15")],
        [InlineKeyboardButton(text="20 Birr", callback_data="20"),
         InlineKeyboardButton(text="25 Birr", callback_data="25"),
         InlineKeyboardButton(text="50 Birr", callback_data="50")],
        [InlineKeyboardButton(text="100 Birr", callback_data="100"),
         InlineKeyboardButton(text="500 Birr", callback_data="500"),
         InlineKeyboardButton(text="1000 Birr", callback_data="1000")]
    ]
    return InlineKeyboardMarkup(recharge_key)


def cancel(update: Update, context: CallbackContext) -> int:
    update.message.reply_text("Conversation canceled.")
    return ConversationHandler.END

def main():
    updater = Updater(token="6796089767:AAGMhYGI9KCV2MEuFSNy3_T10DFiSHDvJGM", use_context=True)
    dp = updater.dispatcher

    dp.add_handler(MessageHandler(Filters.contact, contact_callback, pass_user_data=True))
    dp.add_handler(CommandHandler('start', start))
    dp.add_handler(CallbackQueryHandler(handle_button_click))
    dp.add_handler(MessageHandler(Filters.location | Filters.text, message_handler, pass_chat_data=True))
    
    conv_handler = ConversationHandler(
        entry_points=[MessageHandler(Filters.text & ~Filters.command, message_handler)],
        states={
            PHONE_NUMBER: [MessageHandler(Filters.text & ~Filters.command, message_overtaken)],
            
        },
        fallbacks=[CommandHandler('cancel', cancel)],)  
    dp.add_handler(conv_handler)

    print('Polling...')
    updater.start_polling()
    updater.idle()


if __name__ == "__main__":
    main()

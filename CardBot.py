from telegram import InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, Location, ReplyKeyboardMarkup, Update, InputMediaPhoto
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, CallbackContext, Updater, CommandHandler, MessageHandler, \
    Filters, ConversationHandler, CallbackQueryHandler
import re
import asyncio
import logging
import requests
import time
import json
import threading
PHONE_NUMBER = range(1)
PHONE, AMOUNT = range(2)
phoneNumber = ""
CONTACT_INFO_PROCESSED = False
cardValue =""
Safaricom =""
EthioTelecom = ""
cardType = ""
count=0
dict_user = {}

def main_menu():
                    main_keyboard = [
                        [KeyboardButton(text="Ethiotelecom Airtime TopUp "), KeyboardButton(text="Safaricom Airtime TopUp")],
                        [KeyboardButton(text="Check your balance"), KeyboardButton(text="Transfer to the Cardbirr wallet")],
                         [KeyboardButton(text="Help")]
                    ]
                    return ReplyKeyboardMarkup(main_keyboard)
                                
def get_keyboard():
    reply_keyboard = [[ KeyboardButton(text='Do you agree to share your phone number?', request_contact=True, id=1)]]
    return ReplyKeyboardMarkup(reply_keyboard, resize_keyboard=True, one_time_keyboard=True)


def message_overtaken(update: Update, context: CallbackContext):
        global count, phoneNumber, cardType, cardValue # Add this line
        users = update.message.from_user
        dict_user[users.id] = count
    # if update.message.text == 'Ethiotelecom Airtime TopUp' or 'Safaricom Airtime TopUp':
        dict_user[users.id] = count+1
        phoneNumber = str(update.message.text)
        if re.match(r'^\d{10}$', phoneNumber):
            context.user_data['phoneNumber'] = phoneNumber
            phoneNumber = phoneNumber
            telegramUserId = str(update.effective_user.id)
            
            api_url = "https://cardapi.zowibot.com/api/v1/cards/recharge"
            data = {
                "cardValue": cardValue,
                "cardType": cardType,
                "phoneNumber": phoneNumber
            }
            headers = { 'Content-Type': 'application/json', 
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36',
               'telegram_user_id': telegramUserId }
            try:
                response = requests.post(api_url, json=data, headers=headers)
                # print(response.status_code, "code Status")
                err = response.text
                response.raise_for_status()

                if response.status_code == 200:
                    context.bot.send_message(
                        chat_id=update.effective_user.id,
                        text="phone number successfully charged"
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
            context.bot.send_message(chat_id=update.effective_user.id, text=f"Invalid phone number format. Please enter a 10-digit phone number.")
        return PHONE_NUMBER

    
def contact_callback(update: Update, context: CallbackContext):
        global PHONE
        if update.message.contact:
            PHONE = update.message.contact.phone_number
            phoneNumber = PHONE
            telegramUserId = str(update.effective_user.id)
            firstName = update.effective_user.first_name
            api_url = "https://cardapi.zowibot.com/api/v1/users"
            data = {
                'phoneNumber': phoneNumber,
                'telegramUserId': telegramUserId,
                'firstName': firstName,
            }
            headers = {
                'Content-Type': 'application/json',
            }
            try:
                response = requests.post(api_url, json=data, headers=headers)
                if response.status_code == 201:
                    context.bot.send_message(chat_id=update.effective_user.id, text="Please choose your preferred service.", reply_markup=main_menu())
            except requests.exceptions.RequestException as e:
                  context.bot.send_message(chat_id=update.effective_user.id, text=f"Error submitting phone number: {e}")
        else:
            context.bot.send_message(chat_id=update.effective_user.id, text=f"No contact information received.")

            
def cancel(update: Update, context: CallbackContext) -> int:
    update.message.reply_text("Conversation canceled.")
    return ConversationHandler.END

            
def start(update: Update, context: CallbackContext):
        context.bot.send_message(chat_id=update.effective_user.id, text= "Welcome to the Card Birr Bot!", reply_markup=get_keyboard())
    
list_button_click = ["5","10","15","25","50","100","500","1000"]

def card_type(update, context):
    text = update.message.text
    global cardType
    if text == "Ethiotelecom Airtime TopUp":
        cardType ='Ethio_Telecom'
    elif text == "Safaricom Airtime TopUp":
        cardType ='Safaricom'
    return cardType

def card_value(update, context):
    global cardValue
    query = update.callback_query
    query.answer()
    payload = query.data
    if payload in list_button_click:
      cardValue = payload
    return cardValue

             
def handle_button_click(update: Update, context: CallbackContext):
    global cardValue, cardType, phoneNumber
    cardValue =  card_value(update, context)
    query = update.callback_query
    query.answer()
    payload = query.data
    userId = update.effective_user.id
    if payload in list_button_click:
        cardValue= payload
        context.bot.send_message(chat_id=update.effective_user.id, text=f"your card amount {cardValue} Birr, please enter phone number.")
        # context.bot.send_message(chat_id=update.effective_user.id, text="please enter phone Number")
    
              
def send_data_to_api(user_id, phone, amount, update, context):
    
    api_trans = "https://cardapi.zowibot.com/api/v1/transactions"
    data = {
           "amount": amount,
          "phoneNumber": phone
         }
    headers = { 'Content-Type': 'application/json', 
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36',
               'telegram_user_id': user_id }
    response = requests.post(api_trans, json=data, headers=headers)
    err = response.text
    if response.status_code == 200:
    
         return response.json()
    else:
        context.bot.send_message(
                    chat_id=update.effective_user.id,
                    text=f"{json.loads(err).get('message')}")
        
    
def message_handler(update: Update, context: CallbackContext):
    global count
    users = update.message.from_user
    global EthioTelecom, Safaricom, count, phoneNumber
    cardType = card_type(update, context)
    user_id =  str(update.effective_user.id)
    action = context.user_data.get('action')
    text = update.message.text              
    phoneNumber = str(update.message.text)
    if text=="Ethiotelecom Airtime TopUp":
                ethio_telecom_key = [ [InlineKeyboardButton(text="5 Birr", callback_data="5"), 
                                        InlineKeyboardButton(text="10 Birr", callback_data="10"), 
                                        InlineKeyboardButton(text="15 Birr", callback_data="15"),
                                        ],
                                        [
                                        InlineKeyboardButton(text="25 Birr", callback_data="25"),
                                        InlineKeyboardButton(text="50 Birr", callback_data="50"),
                                        InlineKeyboardButton(text="100 Birr", callback_data="100"), 

                                        ],
                                         [
                                        InlineKeyboardButton(text="500 Birr", callback_data="500"),
                                        InlineKeyboardButton(text="1000 Birr", callback_data="1000")
                                        ]
                                       ]
                reply_markup = InlineKeyboardMarkup(ethio_telecom_key)
                context.bot.send_message(chat_id=update.effective_user.id, text=f"seleect card amount.", reply_markup=reply_markup) 
                return PHONE_NUMBER

    elif text=="Safaricom Airtime TopUp":
                safaricom_key =         [ [InlineKeyboardButton(text="5 Birr", callback_data="5"), 
                                        InlineKeyboardButton(text="10 Birr", callback_data="10"), 
                                        InlineKeyboardButton(text="15 Birr", callback_data="15"),
                                        ],
                                        [
                                        InlineKeyboardButton(text="25 Birr", callback_data="25"),
                                        InlineKeyboardButton(text="50 Birr", callback_data="50"),
                                        InlineKeyboardButton(text="100 Birr", callback_data="100"), 

                                        ],
                                         [
                                        InlineKeyboardButton(text="500 Birr", callback_data="500"),
                                        InlineKeyboardButton(text="1000 Birr", callback_data="100")
                                        ]
                                       ]
                reply_markup = InlineKeyboardMarkup(safaricom_key)
                context.bot.send_message(chat_id=update.effective_user.id, text=f"seleect card amount", reply_markup=reply_markup)
                return PHONE_NUMBER
            
    elif text == "Check your balance":
            telegramUserId = str(update.effective_user.id)
            api_url = "https://cardapi.zowibot.com/api/v1/users/me"

            headers = { 'Content-Type': 'application/json', 
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36',
               'telegram_user_id': telegramUserId }
            try:
                response = requests.get(api_url, headers=headers)
                if response.status_code == 200:
                    response = response.json()
                    balance = response['Wallet']['balance']
                    currency = response['Wallet']['currency']
                    context.bot.send_message(chat_id=update.effective_user.id,text= f"Balance: {balance} Birr")
                else:
                    context.bot.send_message(chat_id=update.effective_user.id, text=f"Sorry {update.effective_user.first_name} try again later!")     
                    
            except requests.exceptions.RequestException as e:
                context.bot.send_message(chat_id=update.effective_user.id, text=f"Error submitting phone number: {e}")

                
    elif text == "Transfer to the Cardbirr wallet":
            context.user_data['action'] = 'input_phone'
            context.bot.send_message(chat_id=update.effective_user.id, text=f'Please enter the phone number used for the transfer (e.g., 09xx xx xx xx or 07xx xx xx xx).')
    elif context.user_data.get('action') == 'input_phone':
            phone = text
            if not (phone.isdigit() and len(phone) == 10):
                context.bot.send_message(chat_id=update.effective_user.id, text=f"Please enter a valid 10-digit phone number.")
                return
            context.user_data['phone'] = phone
            context.user_data['action'] = 'input_amount'
            context.bot.send_message(chat_id=update.effective_user.id, text=f'Enter amount')
    elif context.user_data.get('action') == 'input_amount':
            amount = text
            try:
                amount = float(amount)
                if amount <= 5:
                    context.bot.send_message(chat_id=update.effective_user.id, text=f"Please enter amount greater than 5 Birr.")
                    return
            except ValueError:
                context.bot.send_message(chat_id=update.effective_user.id, text=f"Please enter a valid numeric amount.")
                return

            context.user_data['amount'] = amount
            
            response = send_data_to_api(user_id, context.user_data['phone'], context.user_data['amount'], update, context)
            checkout_url = response.get('checkout_url')
            
            keyboard = [[InlineKeyboardButton("Checkout", url=checkout_url)]]
            reply_markup = InlineKeyboardMarkup(keyboard)
            context.bot.send_message(chat_id=update.effective_user.id,  text=f"Click 'Checkout' to continue.", reply_markup=reply_markup)
            context.user_data.clear()
   

    elif text=="Help":
                        context.bot.send_message(chat_id=update.effective_user.id, text =f"Coming Soon")
                                                                     
def main():
    updater = Updater(token="6966499368:AAHLbmayBdrUz_XO5XAKA-zDga60c17v1oI", use_context=True)
    dp = updater.dispatcher
    dp.add_handler(MessageHandler(Filters.contact, contact_callback, pass_user_data=True))
    dp.add_handler(CommandHandler('start', start))
    dp.add_handler(CommandHandler("contact", main_menu))
    dp.add_handler(CallbackQueryHandler(handle_button_click))
    # dp.add_handler(MessageHandler(Filters.location | Filters.text, message_handler, pass_chat_data=True))
    
    conv_handler = ConversationHandler(
    entry_points=[MessageHandler(Filters.text & ~Filters.command, message_handler)],
    states={
        PHONE_NUMBER: [MessageHandler(Filters.text, message_overtaken)],
    },
            fallbacks=[CommandHandler('cancel', cancel)],)  

    dp.add_handler(conv_handler)
    
    print('Polling...')
    updater.start_polling()
    dp.remove_handler(MessageHandler(Filters.contact, contact_callback, pass_user_data=True))
    updater.idle()

if __name__ == "__main__":
    main()
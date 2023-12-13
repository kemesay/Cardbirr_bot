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

def service():
                    main_keyboard = [
                        [InlineKeyboardButton(text="09xx..or 07xx.. service ", callback_data="start_phone")                                       ]
                        ]
                    return InlineKeyboardMarkup(main_keyboard)

def main_menu():
                    main_keyboard = [
                        [KeyboardButton(text="Ethio telecom Top Ups"), KeyboardButton(text="Safari com Top Ups")],
                        [KeyboardButton(text=" Ckeck Balance"), KeyboardButton(text="Transfer Banks to Wallet")],
                         [KeyboardButton(text="Help")]
                    ]
                    return ReplyKeyboardMarkup(main_keyboard)
                                
def get_keyboard():
    reply_keyboard = [[ KeyboardButton(text='Are you agree to share your Phone Number', request_contact=True, id=1)]]
    return ReplyKeyboardMarkup(reply_keyboard, resize_keyboard=True, one_time_keyboard=True)


def get_phone_number(update: Update, context: CallbackContext):
    global cardType
    phone_number = update.message.text
    context.bot.send_message(chat_id=update.effective_user.id, text=f"Phone number: {phone_number}")
    cardType = message_handler(update, context)
    return ConversationHandler.END


def message_overtaken(update: Update, context: CallbackContext):
    global count, phoneNumber, cardType, cardValue # Add this line
    users = update.message.from_user
    dict_user[users.id] = count
    if update.message.text == 'Ethio telecom Top Ups' or 'Safari com Top Ups':
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
                print(response.status_code, "code Status")
                err = response.text
                response.raise_for_status()

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
    return PHONE_NUMBER


    


def contact_callback(update: Update, context: CallbackContext):
        global PHONE
        if update.message.contact:
            PHONE = update.message.contact.phone_number
            print(f"Phone number: {PHONE}")
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
                print(response.text)
                print("response", response.json())
                if response.status_code == 201:
                    context.bot.send_message(chat_id=update.effective_user.id, text="Select the service you want!", reply_markup=main_menu())
            except requests.exceptions.RequestException as e:
                print(f"Error submitting phone number: {e}")
        else:
            print("No contact information received.")
            
def cancel(update: Update, context: CallbackContext) -> int:
    update.message.reply_text("Conversation canceled.")
    return ConversationHandler.END

            
def start(update: Update, context: CallbackContext):
        context.bot.send_message(chat_id=update.effective_user.id,
                                 text=f"Hello Mr/Mrs. {update.effective_user.first_name} \n Welcome to the Card Birr Bot!", reply_markup=get_keyboard())
    
list_button_click = ["5","10","15","20","25","50","100","500","1000"]

list_service = ["ethio", "safari"]

def card_type(update, context):
    text = update.message.text
    global cardType
    if text == "Ethio telecom Top Ups":
        cardType ='Ethio_Telecom'
    elif text == "Safari com Top Ups":
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
        context.bot.send_message(chat_id=update.effective_user.id, text=f"You have selected {cardValue} Birr from {cardType}")
        context.bot.send_message(chat_id=update.effective_user.id, text="please enter the phone Number you want to charge")
    elif payload in list_service:
                context.bot.send_message(chat_id=update.effective_user.id, text="please enter the phone Number you want to charge")

    elif query.data == 'start_phone':
        context.user_data['action'] = 'input'
        query.edit_message_text(text='Send me your phone number:')
        
    
            
            
            
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
    # print(response.text, "hhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhh")
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

    if action == 'input':
        if 'phone' not in context.user_data:
            phone = update.message.text

            # Validate phone number
            if not (phone.isdigit() and len(phone) == 10):
                update.message.reply_text("Please enter a valid 10-digit phone number.")
                return
            context.user_data['phone'] = phone
            update.message.reply_text('Now, send me the amount you want to transfer')
        elif 'amount' not in context.user_data:
            amount = update.message.text

            # Validate amount (integer, greater than $5)
            try:
                amount = float(amount)
                if amount <= 5:
                    update.message.reply_text("Please enter an amount greater than $5.")
                    return
            except ValueError:
                update.message.reply_text("Please enter a valid numeric amount.")
                return
            context.user_data['amount'] = amount
            
            response = send_data_to_api(user_id, context.user_data['phone'], context.user_data['amount'], update, context)
            checkout_url = response.get('checkout_url')
            
            keyboard = [[InlineKeyboardButton("Checkout", url=checkout_url)]]
            reply_markup = InlineKeyboardMarkup(keyboard)
            update.message.reply_text("Phone number and amount received successfully! Click 'Checkout' to proceed.", reply_markup=reply_markup)
            context.user_data.clear()


    elif text=="Ethio telecom Top Ups":
                ethio_telecom_key = [ [InlineKeyboardButton(text="5 Birr", callback_data="5"), 
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
                update.message.reply_text("You Can select, the card amount you want to fill", reply_markup=reply_markup) 
                return PHONE_NUMBER
                # return ConversationHandler.END

    elif text=="Safari com Top Ups":
                safaricom_key =         [ [InlineKeyboardButton(text="5 Birr", callback_data="5"), 
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
                update.message.reply_text("You Can select, the card amount you want  to fill", reply_markup=reply_markup)
                return PHONE_NUMBER
            
    elif text == "Ckeck Balance":
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
                    context.bot.send_message(chat_id=update.effective_user.id, text=f"Hello {update.effective_user.first_name} your current balance is  {balance} {currency}")
                else:
                    context.bot.send_message(chat_id=update.effective_user.id, text=f"Sorry {update.effective_user.first_name} try again later!")     
                    
            except requests.exceptions.RequestException as e:
                print(f"Error submitting phone number: {e}")
                
    elif text=="Transfer Banks to Wallet":
        
        context.bot.send_message(chat_id=update.effective_user.id, text=f"{update.effective_user.first_name} select the service you want need", reply_markup=service())     


    elif text=="Help":
                        update.message.reply_text(text ="Coming Soon")
                                                                     
def main():
    updater = Updater(token="6680224136:AAH95LjUiyLSC8PuyMy10jXxx4-op2i-teI", use_context=True)
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
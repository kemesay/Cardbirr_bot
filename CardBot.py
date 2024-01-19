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

cardbirr_support_bot_link = "https://t.me/Cardbirrsupport_bot"


def main_menu():
             main_keyboard = [
                        [KeyboardButton(text="Ethiotelecom Airtime TopUp "), KeyboardButton(text="Safaricom Airtime TopUp")],
                        [KeyboardButton(text="Check your balance"), KeyboardButton(text="Bank deposit to your account")],
                         [KeyboardButton(text="Contact Us"), KeyboardButton(text="Description")],
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
                print(response.json(), "check code")
                err = response.text
                
                if response.status_code == 200:
                    respo = response.json()
                    ussd_command = respo['command']
                    response.raise_for_status()
                    message_text = f"Click the link to charge your Safaricom phone: \n\n{ussd_command}"
                    context.bot.send_message(chat_id=update.effective_user.id, text =f"{ussd_command}")
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
            return
            
        return PHONE_NUMBER

    
def contact_callback(update: Update, context: CallbackContext):
        global PHONE
        if update.message.contact:
            PHONE = update.message.contact.phone_number
            phoneNumber = PHONE
            telegramUserId = str(update.effective_user.id)
            firstName = update.effective_user.first_name
            api_url = "https://cardapi.zowibot.com/api/v1/users"
            print(phoneNumber, firstName)
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
        CHAT_ID = update.effective_user.id
        print(CHAT_ID, "yyyyyyyyyyyyyyyyyyyyyy")
        context.bot.send_message(chat_id=update.effective_user.id, text= "Welcome to the Card Birr Bot!", reply_markup=get_keyboard())

def start1(update: Update, context: CallbackContext):
        context.bot.send_message(chat_id=update.effective_user.id, text= "Cardbirr Successfully Restarted!", reply_markup=main_menu())
    
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
        context.bot.send_message(chat_id=update.effective_user.id, text=f"You selected {cardValue} Birr, please enter your phone number.")
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
        response = response.json()
        checkout_url = response.get('checkout_url')
        keyboard = [[InlineKeyboardButton("Checkout", url=checkout_url)]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        context.bot.send_message(chat_id=update.effective_user.id,  text=f"Click 'Checkout' to complete payment on the web portal.", reply_markup=reply_markup)
    
          
    else:
        context.bot.send_message(
                    chat_id=update.effective_user.id,
                    text=f"{json.loads(err).get('message')}")

def timeout_callback(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Conversation timed out. Please restart the process.")

        
    
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
        
                apifor= f'https://cardapi.zowibot.com/api/v1/cards/available-prices?cardType={cardType}'
                
                response = requests.get(apifor)
             
                if response.status_code == 200:
                    available_prices = response.json()
                    list_button_click = ["5", "10", "15", "25", "50", "100", "500", "1000"]
                    if not available_prices:
                        context.bot.send_message(chat_id=update.effective_user.id, text="Ethio telecom cards unavailable at the moment. Restocking shortly.")
                        return
                   
                    else:
                        list_button_click = [str(price) for price in available_prices]
                        ethio_telecom_key = []
                        row = []
                        for price in list_button_click:
                            button = InlineKeyboardButton(text=f"{price} Birr", callback_data=price)
                            row.append(button)
                            if len(row) == 3:
                                ethio_telecom_key.append(row)
                                row = []

                        if row:
                            ethio_telecom_key.append(row)

                        reply_markup = InlineKeyboardMarkup(ethio_telecom_key)

                        context.bot.send_message(chat_id=update.effective_user.id, text=f"Select card amount", reply_markup=reply_markup)
                        
                else:
                         context.bot.send_message(chat_id=update.effective_user.id, text=f"Failed to retrieve data. Status code: {response.status_code}")
                         return
                return PHONE_NUMBER 

    elif text=="Safaricom Airtime TopUp":
        
                apifor= f'https://cardapi.zowibot.com/api/v1/cards/available-prices?cardType={cardType}'
                
                response = requests.get(apifor)

                if response.status_code == 200:
                    available_prices = response.json()
                    list_button_click = ["5", "10", "15", "25", "50", "100", "500", "1000"]
                    if not available_prices:
                        context.bot.send_message(chat_id=update.effective_user.id, text="Safaricom cards unavailable at the moment. Restocking shortly.")
                        return
                   
                    else:
                        list_button_click = [str(price) for price in available_prices]
                        ethio_telecom_key = []
                        row = []
                        for price in list_button_click:
                            button = InlineKeyboardButton(text=f"{price} Birr", callback_data=price)
                            row.append(button)
                            if len(row) == 3:
                                ethio_telecom_key.append(row)
                                row = []

                        if row:
                            ethio_telecom_key.append(row)

                        reply_markup = InlineKeyboardMarkup(ethio_telecom_key)

                        context.bot.send_message(chat_id=update.effective_user.id, text=f"Select card amount", reply_markup= reply_markup)
                else:
                     context.bot.send_message(chat_id=update.effective_user.id, text=f"Failed to retrieve data. Status code: {response.status_code}")
                     return
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

                
    elif text == "Bank deposit to your account":
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
                if amount < 5:
                    context.bot.send_message(chat_id=update.effective_user.id, text=f"The minimum allowed amount is 5 Birr.")
                    return
            except ValueError:
                context.bot.send_message(chat_id=update.effective_user.id, text=f"Please enter a valid numeric amount.")
                return

            context.user_data['amount'] = amount
            
            response = send_data_to_api(user_id, context.user_data['phone'], context.user_data['amount'], update, context)
            context.user_data.clear()
   

    elif text=="Contact Us":
                         user = update.message.from_user
                         print(user)
                         button = InlineKeyboardButton("Cardbirr Support Bot", url=cardbirr_support_bot_link)
                         reply_markup = InlineKeyboardMarkup([[button]])
                         context.bot.send_message(chat_id=update.effective_user.id, text =f"click button to get support", reply_markup=reply_markup)
                         
    elif text=="Description":
                        context.bot.send_message(chat_id=update.effective_user.id, text =f"Coming Soon")
                                                                     
def main():
    updater = Updater(token="6709665712:AAE1c4WP68WJ4UzJsoGWPJlAmyYvmC9GnlE", use_context=True)
    dp = updater.dispatcher
    dp.add_handler(MessageHandler(Filters.contact, contact_callback, pass_user_data=True))
    dp.add_handler(CommandHandler('start', start))
    dp.add_handler(CommandHandler('start1', start1))

    dp.add_handler(CommandHandler("contact", main_menu))
    dp.add_handler(CallbackQueryHandler(handle_button_click))
    # dp.add_handler(MessageHandler(Filters.location | Filters.text, message_handler, pass_chat_data=True))
    
    conv_handler = ConversationHandler(
    entry_points=[MessageHandler(Filters.text & ~Filters.command, message_handler)],
    states={
        PHONE_NUMBER: [MessageHandler(Filters.text, message_overtaken)],
    },
            fallbacks=[CommandHandler('cancel', cancel)],
            
            per_chat=True,  # Set to True if you want the timeout to be per chat
            conversation_timeout=8,  # Set the timeout value in seconds

            )  

    dp.add_handler(conv_handler)
    
    print('Polling...')
    updater.start_polling()
    dp.remove_handler(MessageHandler(Filters.contact, contact_callback, pass_user_data=True))
    updater.idle()

if __name__ == "__main__":
    main()
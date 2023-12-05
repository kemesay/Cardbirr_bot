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
phoneNumber = ""
CONTACT_INFO_PROCESSED = False
cardValue =""
Safaricom =""
EthioTelecom = ""
cardType = ""
count=0
dict_user = {}
def spinning_win_button():
                            btn = [
                                [InlineKeyboardButton(text="Play Spining", callback_data="Playsw")],
                            ]
                            return InlineKeyboardMarkup(btn)
def depo_button():
                    btn = [
                        [InlineKeyboardButton(text="Deposit", callback_data="transfer")],
                    ]
                    return InlineKeyboardMarkup(btn)
                
def userRegister():
                    btn = [
                        [InlineKeyboardButton(text="Register yourself", callback_data="registration")],
                    ]
                    return InlineKeyboardMarkup(btn)


def main_menu():
                    main_keyboard = [
                        [KeyboardButton(text="Ethio telecom Top Ups"), KeyboardButton(text="Safari com Top Ups")],
                        [KeyboardButton(text=" Account"), KeyboardButton(text="Help")]
                    ]
                    return ReplyKeyboardMarkup(main_keyboard)

def account_menu():
                    main_keyboard = [
                        [InlineKeyboardButton(text="Check your Balance", callback_data="Balance"), 
                        InlineKeyboardButton(text="Transfer Banks to Wallet", callback_data="transfertowallet"), 
                                                ]
                        ]
                    return InlineKeyboardMarkup(main_keyboard)
                
def recharge_menu():
                    main_keyboard = [
                        [InlineKeyboardButton(text="This phone", callback_data="thisphone"), 
                        InlineKeyboardButton(text="Other phone", callback_data="otherphone"), 
                                                ]
                        ]
                    return InlineKeyboardMarkup(main_keyboard)
                
def get_keyboard():
    reply_keyboard = [[ KeyboardButton(text='Are you agree to share your Phone Number', request_contact=True, id=1)]]
    return ReplyKeyboardMarkup(reply_keyboard, resize_keyboard=True, one_time_keyboard=True)
# Add a global flag to track whether contact information has been processed


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






def message_overtaken(update: Update, context: CallbackContext):
    global count, phoneNumber, cardType, cardValue # Add this line
    users = update.message.from_user
    dict_user[users.id] = count
    # print("text from overtaken message", update.message.text )
    if update.message.text == 'Ethio telecom Top Ups' or 'Safari com Top Ups':
        dict_user[users.id] = count+1
        phoneNumber = str(update.message.text)
        if re.match(r'^\d{10}$', phoneNumber):
            context.user_data['phoneNumber'] = phoneNumber

            phoneNumber = phoneNumber
            print(phoneNumber, "lasttttttttttttttttttttttttt")
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
            print(data,headers, "dddddddddddddddhhhhhhhhhhhh")
            try:
                response = requests.post(api_url, json=data, headers=headers)
                response.raise_for_status()
                print(response.text)
                print("response", response.json())
                if response.status_code == 201:
                    context.bot.send_message(
                        chat_id=update.effective_user.id,
                        text="The phone is successfully charged!",
                        reply_markup=main_menu()
                    )
                    return ConversationHandler.END
            except requests.exceptions.RequestException as e:
                print(f"Error submitting phone number: {e}")

        else:
            update.message.reply_text("Invalid phone number format. Please enter a 10-digit phone number.")
        
    return PHONE_NUMBER





# CONTACT_INFO_PROCESSED = False
def contact_callback(update: Update, context: CallbackContext):
        global PHONE
    # if not CONTACT_INFO_PROCESSED:
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
    # else:
    #     print("Contact information already processed.")

def start(update: Update, context: CallbackContext):
        context.bot.send_message(chat_id=update.effective_user.id,
                                 text=f"Hello Mr/Mrs. {update.effective_user.first_name} \n Welcome to the Card Birr Bot!", reply_markup=get_keyboard())
    
list_button_click = ["5","10","15","20","25","50","100","500","1000"]

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
        print("yuuuuuuuuuuuuuuuuuuuuuuuuu", phoneNumber) 
        
       
    elif query.data == "Balance":
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
                
                
                
        
    elif query.data == "transfertowallet":
        context.bot.send_message(chat_id=update.effective_user.id, text=f"Mr/Mrs. {update.effective_user.first_name}")
        
                                                     
def message_handler(update: Update, context: CallbackContext):
    global EthioTelecom, Safaricom, count, phoneNumber
    cardType = card_type(update, context)
    print(cardType, "card type..................")
    phoneNumber = str(update.message.text)
    print(phoneNumber, "I am phone Numberrrrrrrrrrrrrrrrrrrrrr")

    
    text = update.message.text              
    if text=="Ethio telecom Top Ups":
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
                
                # return PHONE_NUMBER
                return ConversationHandler.END


                
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
                
                # return PHONE_NUMBER
                return ConversationHandler.END

                
    elif text=='Ethio telecom Top Ups' or 'Safari com Top Ups' and  count == 0:
        return message_overtaken(update, context)
                
                               
    elif text=="Account":
                        update.message.reply_text(text ="You can check Amount or Transfer your balance from Banks to this wallet", reply_markup=account_menu())
    elif text=="Help":
                        update.message.reply_text(text ="Coming Soon")
    
    # return PHONE_NUMBER
                                            
def main():
    updater = Updater(token="6796089767:AAGMhYGI9KCV2MEuFSNy3_T10DFiSHDvJGM", use_context=True)
    dp = updater.dispatcher
    dp.add_handler(MessageHandler(Filters.contact, contact_callback, pass_user_data=True))
    dp.add_handler(CommandHandler('start', start))
    dp.add_handler(CommandHandler("contact", main_menu))
    dp.add_handler(CallbackQueryHandler(handle_button_click))
    dp.add_handler(MessageHandler(Filters.location | Filters.text, message_handler, pass_chat_data=True))
    
    conv_handler = ConversationHandler(
    entry_points=[MessageHandler(Filters.text & ~Filters.command, message_overtaken)],
    states={
        PHONE_NUMBER: [MessageHandler(Filters.text, message_handler)],
    },
    fallbacks=[],
    )

    dp.add_handler(conv_handler)
    
    
    print('Polling...')
    updater.start_polling()
    dp.remove_handler(MessageHandler(Filters.contact, contact_callback, pass_user_data=True))
    updater.idle()

if __name__ == "__main__":
    main()
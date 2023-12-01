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

#################################################################################################################################### Login With locally Stored Password
PHONE_NUMBER = range(1)

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


def start(update: Update, context: CallbackContext):
    
        context.bot.send_message(chat_id=update.effective_user.id,
                                 text=f"Hello Mr/Mrs. {update.effective_user.first_name} \n Welcome to the Card filling Bot \n Please enter your phone number to register")
        return PHONE_NUMBER
    
def phone_number_received(update: Update, context: CallbackContext) -> int:
    if 'phone_number' in context.user_data:
        return ConversationHandler.END

    phone_number = str(update.message.text)

    if re.match(r'^\d{10}$', phone_number):
        context.user_data['phone_number'] = phone_number

        phoneNumber = phone_number
        telegramUserId = str(update.effective_user.id)
        firstName = update.effective_user.first_name

        api_url = "https://cardapi.zowibot.com/api/v1/users"
        data = {
            'phoneNumber': phoneNumber,
            'telegramUserId': '10010404799',
            'firstName': firstName,
        }
        headers = {
            'Content-Type': 'application/json',
        }
        try:
            response = requests.post(api_url, json=data, headers=headers)
            response.raise_for_status()
            print("response", response.json())
            if response.status_code == 201:
                context.bot.send_message(
                    chat_id=update.effective_user.id,
                    text="You are successfully registered for this Service by the phone you Input!",
                    reply_markup=main_menu()
                )
                return ConversationHandler.END
        except requests.exceptions.RequestException as e:
            print(f"Error submitting phone number: {e}")

    else:
        update.message.reply_text("Invalid phone number format. Please enter a 10-digit phone number.")
    
    return PHONE_NUMBER


def cancel(update: Update, context: CallbackContext) -> int:
    update.message.reply_text("Conversation canceled.")
    return ConversationHandler.END
        

list_button_click = ["5","10","15","20","25","50","100","500","1000"]
           
selected_number  = 0            
                
def handle_button_click(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()
    payload = query.data
    userId = update.effective_user.id
    

    if payload in list_button_click:
        selected_number= payload
        context.bot.send_message(chat_id=update.effective_user.id, text=f"You have selected {selected_number}")
            
        return selected_number
    
    elif query.data == "Balance":
        context.bot.send_message(chat_id=update.effective_user.id, text=f"Mr/Mrs. {update.effective_user.first_name}")
        message, drawnNumber, drawnNumberPrizenumber, drawnNumberPrize, userwalletBalance, userwalletCurrency = send_spinning_win_description(userId)
        context.bot.send_message(chat_id=update.effective_user.id,  text=f" message:{message}  \ndrawnNumber:{drawnNumber}, \nyour drawn Prize number is:{drawnNumberPrizenumber} \nyour prize is :{drawnNumberPrize} \nyour current wallete balance is:{userwalletBalance} \nyour currency is: {userwalletCurrency}")
   
   
    elif query.data == "transfertowallet":
        context.bot.send_message(chat_id=update.effective_user.id, text=f"Mr/Mrs. {update.effective_user.first_name}")
        message, drawnNumber, drawnNumberPrizenumber, drawnNumberPrize, userwalletBalance, userwalletCurrency = send_spinning_win_description(userId)
        context.bot.send_message(chat_id=update.effective_user.id,  text=f" message:{message}  \ndrawnNumber:{drawnNumber}, \nyour drawn Prize number is:{drawnNumberPrizenumber} \nyour prize is :{drawnNumberPrize} \nyour current wallete balance is:{userwalletBalance} \nyour currency is: {userwalletCurrency}")
        
        
    elif query.data == "thisphone":
        # context.bot.send_message(chat_id=update.effective_user.id, text ="Coming Soon")
        api_url = "https://cardapi.zowibot.com/api/v1/users/me"

        headers = { 'Content-Type': 'application/json', 
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36',
               'telegram_user_id': '10010404799' }
        
        response = requests.get(api_url, headers=headers)
        print("response", response.json())

        response.raise_for_status()
        # print(response)
        if response.status_code == 200:
            data=response.json()
            phoneNumber=data['phoneNumber']
            
            api_url= "https://cardapi.zowibot.com/api/v1/cards/recharge"
            headers = { 'Content-Type': 'application/json',
                        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36',
               'telegram_user_id': '10010404799'}
            data =    {"cardValue": "500",
                        "cardType": "Safaricom",
                        "phoneNumber": phoneNumber}
            
            
            response = requests.post(api_url,json=data, headers=headers)
            response.raise_for_status()
            if response.status_code == 200:

               context.bot.send_message(chat_id=update.effective_user.id, text="your successfully recahrge your phone")
            elif response.status_code == 400: 
                context.bot.send_message(chat_id=update.effective_user.id, text="Insufficient funds: Your current balance is 400.00") 
            else: 
                context.bot.send_message(chat_id=update.effective_user.id, text="some Error occured") 


                                
    elif query.data == "otherphone":
                                context.bot.send_message(chat_id=update.effective_user.id, text ="Coming Soon")

        
  
def message_handler(update: Update, context: CallbackContext):
    users = update.message.from_user
    message_type = update.message.chat.type
    contact = update.effective_message.contact
    phone = contact.phone_number
    print(phone, "phone numberrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrr")
    
    text = update.message.text
    if text=="Ethio telecom Top Ups":
                
               main_keyboard = [
                        [InlineKeyboardButton(text="This phone", callback_data="thisphone"), 
                        InlineKeyboardButton(text="Other phone", callback_data="otherphone"), 
                                                ]
                        ]
               reply_markup = InlineKeyboardMarkup(main_keyboard)
               update.message.reply_text("You Can select, the phone you want to recharge", reply_markup=reply_markup)

                
    # if text=="Ethio telecom Top Ups":
                
    #             ethio_telecom_key = [ [InlineKeyboardButton(text="5 Birr", callback_data="5"), 
    #                                     InlineKeyboardButton(text="10 Birr", callback_data="10"), 
    #                                     InlineKeyboardButton(text="15 Birr", callback_data="15"),
    #                                     ],
    #                                     [
    #                                     InlineKeyboardButton(text="20 Birr", callback_data="20"),
    #                                     InlineKeyboardButton(text="25 Birr", callback_data="25"),
    #                                     InlineKeyboardButton(text="50 Birr", callback_data="50"),
    #                                     ],
                                         
    #                                      [
    #                                     InlineKeyboardButton(text="100 Birr", callback_data="100"), 
    #                                     InlineKeyboardButton(text="500 Birr", callback_data="500"),
    #                                     InlineKeyboardButton(text="1000 Birr", callback_data="1000")
    #                                     ]
    #                                    ]
    #             reply_markup = InlineKeyboardMarkup(ethio_telecom_key)
    #             update.message.reply_text("You Can select, the card amount you want to fill", reply_markup=reply_markup)
                
                   
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
                update.message.reply_text("You Can select, the card amount yo want  to fill", reply_markup=reply_markup)
                         
                
    elif text=="Account":
                        update.message.reply_text(text ="You can check Amount or Transfer your balance from Banks to this wallet", reply_markup=account_menu())
    elif text=="Help":
                        update.message.reply_text(text ="Coming Soon")
                    
def send_spinning_win_description(userId):
    api_url = 'http://testapi.zowibot.com/api/v1/spin-to-win/place-bet'
    headers = { 'Content-Type': 'application/json', 
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36',
               'telegram_user_id': str(userId) }
    response = requests.post(api_url, headers=headers)
    data = response.json()
    message = data['message']
    drawnNumber = data['drawnNumber']
    drawnNumberPrizenumber = data['drawnNumberPrize']['number']
    drawnNumberPrize = data['drawnNumberPrize']['prize']
    userwalletBalance = data['userWallet']['balance']
    userwalletCurrency = data['userWallet']['currency']
    return message, drawnNumber, drawnNumberPrizenumber, drawnNumberPrize, userwalletBalance, userwalletCurrency
    
    
def main():
    updater = Updater(token="6796089767:AAGMhYGI9KCV2MEuFSNy3_T10DFiSHDvJGM", use_context=True)
    dp = updater.dispatcher
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            PHONE_NUMBER: [MessageHandler(Filters.text & ~Filters.command, phone_number_received)],
            
        },
        fallbacks=[CommandHandler('cancel', cancel)],)  
    dp.add_handler(conv_handler)
  
    dp.add_handler(CallbackQueryHandler(handle_button_click))
    dp.add_handler(MessageHandler(Filters.location | Filters.text, message_handler, pass_chat_data=True))
    print('Polling...')
    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
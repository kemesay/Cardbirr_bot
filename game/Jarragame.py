from telegram import InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, Location, ReplyKeyboardMarkup, Update, InputMediaPhoto
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, CallbackContext, Updater, CommandHandler, MessageHandler, \
    Filters, ConversationHandler, CallbackQueryHandler

import asyncio
import logging
import requests
import time
import json
import threading

#################################################################################################################################### Login With locally Stored Password
def spinning_win_button():
    btn = [
        [InlineKeyboardButton(text="Play Spining", callback_data="Playsw")],
    ]
    return InlineKeyboardMarkup(btn)

def main_menu():
    main_keyboard = [
        [KeyboardButton(text="🌀 Spinning Win"), KeyboardButton(text="🗑 Keno")],
        [KeyboardButton(text=" 🎟 Lotter"), KeyboardButton(text="⚽ Sport Betting")],
        [KeyboardButton(text=" 👛 Your Balance")]
    ]
    return ReplyKeyboardMarkup(main_keyboard)

def start(update: Update, context: CallbackContext):
    username = update.effective_user.username
    print(username)
    context.bot.send_message(chat_id=update.effective_user.id,
                             text=f"Hello Mr/Mrs. {update.effective_user.first_name} \n Wel come to Preferred Bot based Game", reply_markup=main_menu())

list_button_click = ["1","2","3","4","5","6","7","8","9","10","11","12","13","14","15","16","17","18","19","20","21","22","23","24","25","26","27","28","29",
                     "30", "31","32","33","34","35","36","37","38","39","40","41","42","43","44","45","46","47","48","49","50","51","52","53","54","55","56",
                     "57","58","59","60","61","62","63","64","65","66","67","68","69","70","71","72", "73","74", "75","76","77","78","79","80"]
            
selected_numbers = []              
                
def handle_button_click(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()
    payload = query.data
    userId = update.effective_user.id
    print("userId", userId)
    
    # if query.data == "login":
    #    return ready_to_start(update, context)
    if payload in list_button_click:
        # selected_numbers.clear()
        selected_numbers.append(payload)
        print(selected_numbers)
        
        if len(selected_numbers) == 6:
            context.bot.send_message(chat_id=update.effective_user.id, text=f"You have selected {selected_numbers}")
            selected_numbers.clear()
            
    
        return selected_numbers
    
    elif query.data == "Playsw":
        context.bot.send_message(chat_id=update.effective_user.id,
                             text=f"Mr/Mrs. {update.effective_user.first_name}")
        message, drawnNumber, drawnNumberPrizenumber, drawnNumberPrize, userwalletBalance, userwalletCurrency = send_spinning_win_description(userId)
        
        context.bot.send_message(chat_id=update.effective_user.id,  text=f" message:{message}  \ndrawnNumber:{drawnNumber}, \nyour drawn Prize number is:{drawnNumberPrizenumber} \nyour prize is :{drawnNumberPrize} \nyour current wallete balance is:{userwalletBalance} \nyour currency is: {userwalletCurrency} ")
  
def message_handler(update: Update, context: CallbackContext):
    users = update.message.from_user
    message_type = update.message.chat.type
    text = update.message.text
    
    if text=="🌀 Spinning Win":
                
                context.bot.send_message(chat_id=update.effective_user.id,
                              text="Wel come to Spinning to win Bet and you betting 20 Birr for the Following prize:")
                context.bot.send_message(chat_id=update.effective_user.id,
                              text=  "count: 1 number, prize: 500,000 Birr \ncount: 1 number, prize: 100,000 Birr \ncount: 1 number, prize: 50,000 Birr \
                              \ncount: 1 number, prize: 10,000 Birr \ncount: 1 number, prize: 5000 Birr \ncount: 5 numbers, prize: 1000 Birr \ncount: 50 numbers, prize: 500 Birr \
                              \ncount: 100 numbers, prize: 100 Birr"  ,reply_markup=spinning_win_button())
    elif text=="🗑 Keno":
                rate_key =           [ [InlineKeyboardButton(text="1", callback_data="1"), 
                                        InlineKeyboardButton(text="2", callback_data="2"), 
                                        InlineKeyboardButton(text="3", callback_data="3"),
                                        InlineKeyboardButton(text="4", callback_data="4"),
                                        InlineKeyboardButton(text="5", callback_data="5"),
                                        InlineKeyboardButton(text="6", callback_data="6"), 
                                        InlineKeyboardButton(text="7", callback_data="7"), 
                                        InlineKeyboardButton(text="8", callback_data="8")
                                        ],
                                        [
                                        InlineKeyboardButton(text="9", callback_data="9"),
                                        InlineKeyboardButton(text="10", callback_data="10"),
                                        InlineKeyboardButton(text="11", callback_data="11"), 
                                        InlineKeyboardButton(text="12", callback_data="12"), 
                                        InlineKeyboardButton(text="13", callback_data="13"),
                                        InlineKeyboardButton(text="14", callback_data="14"),
                                        InlineKeyboardButton(text="15", callback_data="15"),
                                        InlineKeyboardButton(text="16", callback_data="16") 
                                        ],
                                         [
                                        InlineKeyboardButton(text="17", callback_data="17"), 
                                        InlineKeyboardButton(text="18", callback_data="18"),
                                        InlineKeyboardButton(text="19", callback_data="19"),
                                        InlineKeyboardButton(text="20", callback_data="20") ,    
                                        InlineKeyboardButton(text="21", callback_data="21"), 
                                        InlineKeyboardButton(text="22", callback_data="22"), 
                                        InlineKeyboardButton(text="23", callback_data="23"),
                                        InlineKeyboardButton(text="24", callback_data="24")
                                       
                                        ],
                                        [
                                        InlineKeyboardButton(text="25", callback_data="25"),
                                        InlineKeyboardButton(text="26", callback_data="26"), 
                                        InlineKeyboardButton(text="27", callback_data="27"), 
                                        InlineKeyboardButton(text="28", callback_data="28"),
                                        InlineKeyboardButton(text="29", callback_data="29"),
                                        InlineKeyboardButton(text="30", callback_data="30"),
                                        InlineKeyboardButton(text="31", callback_data="31"), 
                                        InlineKeyboardButton(text="32", callback_data="32") 
                                        ],
                                        [
                                        InlineKeyboardButton(text="33", callback_data="33"),
                                        InlineKeyboardButton(text="34", callback_data="34"),
                                        InlineKeyboardButton(text="35", callback_data="35"),
                                        InlineKeyboardButton(text="36", callback_data="36"), 
                                        InlineKeyboardButton(text="37", callback_data="37"), 
                                        InlineKeyboardButton(text="38", callback_data="38"),
                                        InlineKeyboardButton(text="39", callback_data="39"),
                                        InlineKeyboardButton(text="40", callback_data="40")
                                        
                                        ],
                                         [
                                            
                                        InlineKeyboardButton(text="41", callback_data="41"), 
                                        InlineKeyboardButton(text="42", callback_data="42"), 
                                        InlineKeyboardButton(text="43", callback_data="43"),
                                        InlineKeyboardButton(text="44", callback_data="44"),
                                        InlineKeyboardButton(text="45", callback_data="45"),
                                        InlineKeyboardButton(text="46", callback_data="46"), 
                                        InlineKeyboardButton(text="47", callback_data="47"), 
                                        InlineKeyboardButton(text="48", callback_data="48")
                                        
                                        ],
                                          [
                                            
                                        InlineKeyboardButton(text="49", callback_data="49"),
                                        InlineKeyboardButton(text="50", callback_data="50"),  
                                        InlineKeyboardButton(text="51", callback_data="51"), 
                                        InlineKeyboardButton(text="52", callback_data="52"), 
                                        InlineKeyboardButton(text="53", callback_data="53"),
                                        InlineKeyboardButton(text="54", callback_data="54"),
                                        InlineKeyboardButton(text="55", callback_data="55"),
                                        InlineKeyboardButton(text="56", callback_data="56") 
                                        
                                        ],
                                           [
                                        InlineKeyboardButton(text="57", callback_data="57"), 
                                        InlineKeyboardButton(text="58", callback_data="58"),
                                        InlineKeyboardButton(text="59", callback_data="59"),
                                        InlineKeyboardButton(text="60", callback_data="60"),
                                        InlineKeyboardButton(text="61", callback_data="61"), 
                                        InlineKeyboardButton(text="62", callback_data="62"), 
                                        InlineKeyboardButton(text="63", callback_data="63"),
                                        InlineKeyboardButton(text="64", callback_data="64")
                                        ],
                                           
                                        [
                                        InlineKeyboardButton(text="65", callback_data="65"),
                                        InlineKeyboardButton(text="66", callback_data="66"), 
                                        InlineKeyboardButton(text="67", callback_data="67"), 
                                        InlineKeyboardButton(text="68", callback_data="68"),
                                        InlineKeyboardButton(text="69", callback_data="69"),
                                        InlineKeyboardButton(text="70", callback_data="70"),      
                                        InlineKeyboardButton(text="71", callback_data="71"), 
                                        InlineKeyboardButton(text="72", callback_data="72"), 
                                        ],
                                        
                                        [ 
                                         InlineKeyboardButton(text="73", callback_data="73"),
                                        InlineKeyboardButton(text="74", callback_data="74"),
                                        InlineKeyboardButton(text="75", callback_data="75"),
                                        InlineKeyboardButton(text="76", callback_data="76"), 
                                        InlineKeyboardButton(text="77", callback_data="77"), 
                                        InlineKeyboardButton(text="78", callback_data="78"),
                                        InlineKeyboardButton(text="79", callback_data="79"),
                                        InlineKeyboardButton(text="80", callback_data="80") 
                                        ]
                                           ]
                reply_markup = InlineKeyboardMarkup(rate_key)
                update.message.reply_text("your max selection number is 6 and you expand!", reply_markup=reply_markup)
                         
                
    elif text=="🎟 Lotter":
                        update.message.reply_text(text ="Coming Soon")
    elif text=="⚽ Sport Betting":
                update.message.reply_text(text ="Coming Soon")
    elif text=="👛 Your Balance":
                update.message.reply_text(text ="Coming Soon")
                
                    
def send_spinning_win_description(userId):
    api_url = 'http://testapi.zowibot.com/api/v1/spin-to-win/place-bet'
    headers = { 'Content-Type': 'application/json', 
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36',
               'telegram_user_id': str(userId) }
    response = requests.post(api_url, headers=headers)
    data = response.json()
    print("you see the data of the given system method in above you got:", data)
    message = data['message']
    drawnNumber = data['drawnNumber']
    drawnNumberPrizenumber = data['drawnNumberPrize']['number']
    drawnNumberPrize = data['drawnNumberPrize']['prize']
    userwalletBalance = data['userWallet']['balance']
    userwalletCurrency = data['userWallet']['currency']
    print(message, drawnNumber, drawnNumberPrizenumber, drawnNumberPrize, userwalletBalance, userwalletCurrency)
    return message, drawnNumber, drawnNumberPrizenumber, drawnNumberPrize, userwalletBalance, userwalletCurrency
    
    if response.status_code == 200:
        return True
    else:
        return False
    
def main():
    updater = Updater(token="6622622533:AAEyHKSXzmE2sfb9Ig9zRrsfrjX98wLkDbs", use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CallbackQueryHandler(handle_button_click))
    # dp.add_handler(CallbackQueryHandler(pass_chat_data=True, callback=nearest_of_otc_function, pattern="Playsw"))
    dp.add_handler(MessageHandler(Filters.location | Filters.text, message_handler, pass_chat_data=True))
    print('Polling...')
    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
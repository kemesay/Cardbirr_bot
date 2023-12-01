# def main_menu_keyboard():
#     main_keyboard = [
#         [KeyboardButton(text="Spinnin Win",  callback_data='m1')],
#         [KeyboardButton(text="Keno", callback_data='h1')],
#         [KeyboardButton(text="Lotter", callback_data='b1')],
#         [KeyboardButton(text="Sport Betting",callback_data='m2')],
#         [KeyboardButton(text="W-Balance", callback_data='m3')]]
#     return ReplyKeyboardMarkup(main_keyboard, resize_keyboard=True)


# def main_menu_keyboard():
#     main_keyboard = [
#         [KeyboardButton(text="Spinning Win", callback_data="spinning_win"), 
#          KeyboardButton(text="Keno", callback_data="keno")],
#         [KeyboardButton(text="Lotter", callback_data="lotter"), 
#          KeyboardButton(text="Sport Betting", callback_data="sport_betting")],
#         [KeyboardButton(text="W-Balance", callback_data="w_balance")]
#     ]
#     return ReplyKeyboardMarkup(main_keyboard)



# def message_handler(update: Update, context: CallbackContext):
#     users = update.message.from_user
#     message_type = update.message.chat.type
#     text = update.message.text
#     # if text=="Login":
#     #             update.message.reply_text(text ="Select your Preferred Game!", reply_markup=main_menu_keyboard())
#     if text=="Spinning Win":
#                 update.message.reply_text(text ="Coming Soon")
#     elif text=="Keno":
#                 update.message.reply_text(text ="Coming Soon")
#     elif text=="Lotter":
#                         update.message.reply_text(text ="Coming Soon")
#     elif text=="Sport Betting":
#                 update.message.reply_text(text ="Coming Soon")
#     elif text=="W-Balance":
#                 update.message.reply_text(text ="Coming Soon")



# def handle_button_click(update: Update, context: CallbackContext):
#     query = update.callback_query
#     query.answer()
#     if query.data == "login":
#          context.bot.send_message(chat_id=update.effective_user.id, text="Select your Preferred Game!" ,reply_markup=main_menu_keyboard())


# # def login_button():
# #     btn = [
# #         [KeyboardButton(text="Login", callback_data="login")],
# #     ]
# #     return ReplyKeyboardMarkup(btn, resize_keyboard=True, input_field_placeholder="press Buttons", one_time_keyboard=True)


# def login_button():
#     btn = [
#         [InlineKeyboardButton(text="Login", callback_data="login")],
#     ]
#     return InlineKeyboardMarkup(btn)


# def start(update: Update, context: CallbackContext):
#     username = update.effective_user.username
#     print(username)
#     context.bot.send_message(chat_id=update.effective_user.id,
#                              text=f"Hello Mr/Mrs. {update.effective_user.first_name} \n Wel come to Preferred Bot based Game!")
#     context.bot.send_message(chat_id=update.effective_user.id, text="Click the button to login!" ,reply_markup=login_button())


# def main():
#     updater = Updater(token="6622622533:AAEyHKSXzmE2sfb9Ig9zRrsfrjX98wLkDbs", use_context=True)
#     dp = updater.dispatcher
#     dp.add_handler(CommandHandler("start", start))
#     dp.add_handler(CommandHandler("location", main_menu_keyboard))
#     dp.add_handler(MessageHandler(Filters.location or Filters.text, message_handler, pass_chat_data=True))
#     dp.add_handler(MessageHandler(Filters.text & ~Filters.command, message_handler))
#     dp.add_handler(CallbackQueryHandler(handle_button_click))



#     print('Polling...')
    
#     updater.start_polling()
#     updater.idle()

# if __name__ == "__main__":
#     main()

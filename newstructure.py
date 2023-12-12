from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, MessageHandler, Filters
from telegram.ext import CallbackContext

# Replace 'YOUR_BOT_TOKEN' with your actual bot token
TOKEN = '6680224136:AAH95LjUiyLSC8PuyMy10jXxx4-op2i-teI'

# Replace 'YOUR_API_ENDPOINT' with your actual API endpoint
API_ENDPOINT = 'YOUR_API_ENDPOINT'

def start(update, context):
    user = update.message.from_user
    update.message.reply_text(f"Hi {user.first_name}! Send me your phone number and email address.", reply_markup=inline_buttons())

def inline_buttons():
    keyboard = [
        [
            InlineKeyboardButton("Send Phone Number", callback_data='phone'),
            InlineKeyboardButton("Send Email Address", callback_data='email'),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    return reply_markup

def button_callback(update: Update, context: CallbackContext):
    query = update.callback_query
    user_id = update.effective_user.id

    if query.data == 'phone':
        context.user_data['action'] = 'phone'
        query.edit_message_text(text='Send me your phone number:')
    elif query.data == 'email':
        context.user_data['action'] = 'email'
        query.edit_message_text(text='Send me your email address:')

def handle_text(update, context):
    user_id = update.effective_user.id
    action = context.user_data.get('action')

    if action == 'phone':
        context.user_data['phone'] = update.message.text
        context.user_data['action'] = 'email'
        update.message.reply_text('Now, send me your email address:')
    elif action == 'email':
        context.user_data['email'] = update.message.text
        # Send both phone number and email address to your API endpoint
        # send_data_to_api(user_id, context.user_data['phone'], context.user_data['email'])
        update.message.reply_text("Phone number and email address received successfully!")
    else:
        update.message.reply_text("Please use the inline buttons to choose an action.")

def send_data_to_api(user_id, phone, email):
    # You can customize the API request as per your API specifications
    import requests

    payload = {'user_id': user_id, 'phone': phone, 'email': email}
    # response = requests.post(API_ENDPOINT, json=payload)

def main():
    updater = Updater(TOKEN, use_context=True)

    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_text))
    dp.add_handler(CommandHandler("options", inline_buttons))
    dp.add_handler(CallbackQueryHandler(button_callback))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()

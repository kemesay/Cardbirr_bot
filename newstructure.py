from telegram import InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup, Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext, ConversationHandler
from telegram.ext import JobQueue
import time

# Replace 'YOUR_BOT_TOKEN' with your actual bot token
TOKEN = 'YOUR_BOT_TOKEN'

# Replace 'YOUR_API_ENDPOINT' with your actual API endpoint
API_ENDPOINT = 'YOUR_API_ENDPOINT'

# Define conversation states
INPUT_PHONE, INPUT_AMOUNT = range(2)

def start(update, context):
    user = update.message.from_user
    update.message.reply_text(f"Hi {user.first_name}! Click the button to transfer to the Cardbirr wallet.", reply_markup=inline_buttons())
    return INPUT_PHONE

def inline_buttons():
    keyboard = [
        [KeyboardButton(text="Transfer to the Cardbirr wallet")],
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    return reply_markup

def input_phone(update, context):
    user_id = update.effective_user.id
    message_text = update.message.text

    if message_text == "Transfer to the Cardbirr wallet":
        context.user_data['action'] = 'input_phone'
        update.message.reply_text('Send me your 10-digit phone number:')
        
        # Schedule a job to trigger the timeout in 30 seconds
        context.job_queue.run_once(timeout, 30, context=user_id)
        
        return INPUT_PHONE
    else:
        update.message.reply_text("Please use the button to initiate the transfer.")
        return INPUT_PHONE

def input_amount(update, context):
    user_id = update.effective_user.id
    amount = update.message.text

    # Validate amount (integer, greater than $5)
    try:
        amount = float(amount)
        if amount <= 5:
            update.message.reply_text("Please enter an amount greater than $5.")
            return INPUT_AMOUNT
    except ValueError:
        update.message.reply_text("Please enter a valid numeric amount.")
        return INPUT_AMOUNT

    context.user_data['amount'] = amount
    try:
        # Complete the transaction using phone number and amount
        response = complete_transaction(user_id, context.user_data['phone'], context.user_data['amount'])
        
        # Check the response status
        if response.status_code == 200:
            update.message.reply_text("Transaction completed successfully!")
        else:
            update.message.reply_text(f"Error: {response.status_code} - Unable to complete the transaction. Please try again.")
    except Exception as e:
        update.message.reply_text(f"An error occurred: {str(e)}. Please try again.")

    # Reset the action and user_data for the next input
    context.user_data.clear()
    update.message.reply_text("Ready for a new input. Click 'Transfer to the Cardbirr wallet' to begin.")
    return INPUT_PHONE

def timeout(context: CallbackContext):
    user_id = context.job.context
    context.bot.send_message(chat_id=user_id, text="Timeout! Please restart the process by clicking 'Transfer to the Cardbirr wallet'.")
    context.user_data.clear()
    return INPUT_PHONE

def complete_transaction(user_id, phone, amount):
    # You can customize the API request as per your API specifications
    import requests

    payload = {'user_id': user_id, 'phone': phone, 'amount': amount}
    response = requests.post(API_ENDPOINT, json=payload)
    return response

def main():
    updater = Updater(TOKEN, use_context=True)

    dp = updater.dispatcher

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            INPUT_PHONE: [MessageHandler(Filters.text & ~Filters.command, input_phone)],
            INPUT_AMOUNT: [MessageHandler(Filters.text & ~Filters.command, input_amount)],
        },
        fallbacks=[],
        per_user=False,  # Set to True if you want the timeout to be per user
        per_chat=False,  # Set to True if you want the timeout to be per chat
        conversation_timeout=30,  # Set the timeout value in seconds
    )

    dp.add_handler(conv_handler)

    # Add job queue to the context
    dp.job_queue = JobQueue()
    dp.job_queue.set_dispatcher(dp)
    
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()

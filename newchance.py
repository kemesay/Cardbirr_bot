import logging
import os
import time

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters




def start(update, context):
    
   context.bot.send_message(chat_id=update.effective_user.id  , text='Hi!')


def help(update, context):
    """Sends a message when the command /help is issued."""
    update.message.reply_text('Help!')


# def start_auto(update, context):
#     """Sends a message when the command /start_auto is issued."""
#     n = 0
#     while n < 12:
#         time.sleep(3600)
#         update.message.reply_text('Auto message!')
#         n += 1




def main():
    TOKEN = '6709665712:AAE1c4WP68WJ4UzJsoGWPJlAmyYvmC9GnlE'

    updater = Updater(TOKEN, use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))
    # dp.add_handler(CommandHandler("start_auto", start_auto))

    # log all errors
    # dp.add_error_handler(error)
    print('Polling...')

    updater.idle()


if __name__ == '__main__':
    main()
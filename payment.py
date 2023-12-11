import logging
from telegram import LabeledPrice, ShippingOption, Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters, PreCheckoutQueryHandler, ShippingQueryHandler, CallbackContext, CallbackQueryHandler)

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

def start_callback(update: Update, context: CallbackContext) -> None:
    msg = ("Use /shipping to get an invoice for shipping-payment, or /noshipping for an " "invoice without shipping.")
    update.message.reply_text(msg)

def start_with_shipping_callback(update: Update, context: CallbackContext) -> None:
    chat_id = update.message.chat_id
    title = "Payment Example"
    description = "Payment Example using python-telegram-bot"
    payload = "Custom-Payload"
    provider_token = "YOUR_PROVIDER_TOKEN"
    currency = "ETB"
    price = 1
    prices = [LabeledPrice("Test", price * 100)]

    keyboard = [[InlineKeyboardButton("Shipping", callback_data='shipping'),
                 InlineKeyboardButton("No Shipping", callback_data='noshipping')]]

    reply_markup = InlineKeyboardMarkup(keyboard)

    update.message.reply_invoice(
        title=title,
        description=description,
        payload=payload,
        provider_token=provider_token,
        currency=currency,
        prices=prices,
        need_name=True,
        need_phone_number=True,
        need_email=True,
        need_shipping_address=True,
        is_flexible=True,
        reply_markup=reply_markup
    )

def button_callback(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    chat_id = query.message.chat_id

    if query.data == 'shipping':
        # Handle shipping logic
        options = [ShippingOption('1', 'Shipping Option A', [LabeledPrice('A', 100)])]
        price_list = [LabeledPrice('B1', 150), LabeledPrice('B2', 200)]
        options.append(ShippingOption('2', 'Shipping Option B', price_list))
        context.bot.answer_shipping_query(query.id, ok=True, shipping_options=options)
    elif query.data == 'noshipping':
        # Handle no shipping logic
        context.bot.send_invoice(
            chat_id=chat_id,
            title="Payment Example",
            description="Payment Example using python-telegram-bot",
            payload="Custom-Payload",
            provider_token="YOUR_PROVIDER_TOKEN",
            currency="ETB",
            prices=[LabeledPrice("Test", 100)],
            need_name=True,
            need_phone_number=True,
            need_email=True,
            is_flexible=True
        )
    
    query.answer()

def precheckout_callback(update: Update, context: CallbackContext) -> None:
    query = update.pre_checkout_query
    print(query)

    if query.invoice_payload != 'Custom-Payload':
        query.answer(ok=False, error_message="Something went wrong...")
    else:
        query.answer(ok=True)

def successful_payment_callback(update: Update, context: CallbackContext) -> None:
    update.message.reply_text("Thank you for your payment!")

def main() -> None:
    updater = Updater("YOUR_BOT_TOKEN")
    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler("start", start_callback))
    dispatcher.add_handler(CommandHandler("shipping", start_with_shipping_callback))
    dispatcher.add_handler(CallbackQueryHandler(button_callback))
    dispatcher.add_handler(ShippingQueryHandler(shipping_callback))
    dispatcher.add_handler(PreCheckoutQueryHandler(precheckout_callback))
    dispatcher.add_handler(MessageHandler(Filters.successful_payment, successful_payment_callback))
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()

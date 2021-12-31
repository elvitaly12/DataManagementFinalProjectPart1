import requests
from telegram import Update, ForceReply
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
import logging


def start_command(update: Update, context: CallbackContext):
    context.bot.send_message(chat_id=update.effective_chat.id, text="I'm a bot, please talk to me!")


def help_command(update: Update, context: CallbackContext):
    pass
    # print('do we need this?')


def unregister_cmd(update: Update, context: CallbackContext):
    print("unregister_cmd = ", update['message']['text'])
    user_to_unregister = update['message']['text'].split(' ')[1]
    chat_id = update['message']['chat']['id']
    params = {'UserName': user_to_unregister, 'ChatId': chat_id}
    requests.get(url=' http://127.0.0.1:5000/unregister', params=params)
    # MAYBE NEED TO SWITCH IP


def register_cmd(update: Update, context: CallbackContext):
    print("register_cmd =", update['message']['text'])
    user_to_unregister = update['message']['text'].split(' ')[1]
    chat_id = update['message']['chat']['id']
    params = {'UserName': user_to_unregister, 'ChatId': chat_id}
    requests.get(url=' http://127.0.0.1:5000/register', params=params)
    # MAYBE NEED TO SWITCH IP


def runbot() -> None:
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    updater = Updater('5067453157:AAHvdsy2WlAEvaYa8cDb059hhIlDm1evPNc')

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                        level=logging.INFO)

    # on different commands - answer in Telegram
    dispatcher.add_handler(CommandHandler("start", start_command))
    dispatcher.add_handler(CommandHandler("help", help_command))

    # # on non command i.e message - echo the message on Telegram
    # dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, echo))

    dispatcher.add_handler(CommandHandler("unregister", unregister_cmd))

    dispatcher.add_handler(CommandHandler("register", register_cmd))

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()

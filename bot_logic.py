import requests
from telegram import Update, ForceReply
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
import logging





def start_command(update: Update, context: CallbackContext):
    context.bot.send_message(chat_id=update.effective_chat.id, text="I'm a bot, please talk to me!")

def help_command(update: Update, context: CallbackContext):
    print('do we need this?')


def remove_command(update: Update, context: CallbackContext):
    # print(update['message']['text'])
    user_to_remove= update['message']['text'].split(' ')[1]
    print("ADD SOME LOGIC WITH DB")
    # print(user_to_remove)


    # for key in update:
    #     print(key)


def register_command(update: Update, context: CallbackContext):
    user_to_register = update['message']['text'].split(' ')[1]
    PARAMS={'username' : user_to_register}
    requests.get(url=' http://127.0.0.1:5000/register', params=PARAMS) #MAYBE NEED TO SWITCH IP
    print(update)

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

    dispatcher.add_handler(CommandHandler("remove",remove_command))

    dispatcher.add_handler(CommandHandler("register", register_command))

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()

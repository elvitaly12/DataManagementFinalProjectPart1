import json
import os
import app
import requests
import telegram
from telegram import Update, ForceReply
# from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
from telegram import (
    Poll,
    ParseMode,
    KeyboardButton,
    KeyboardButtonPollType,
    ReplyKeyboardMarkup,
    ReplyKeyboardRemove,
    Update,
)
from telegram.ext import (
    Updater,
    CommandHandler,
    PollAnswerHandler,
    PollHandler,
    MessageHandler,
    Filters,
    CallbackContext,
)
import logging


#####    PART 2 - NEW FUNCS    #######
from config import TELEGRAM_BOT_TOKEN


def poll(update: Update, context: CallbackContext) -> None:
    # print("unregister_cmd = ", update['message']['text'])
    # print("poll update:" ,update)
    # chat_id = update['message']['chat']['id']
    # print(chat_id)
    len2 = len(update['message']['text'].split(' '))
    if len2 <= 1 or len2 > 2:
        context.bot.send_message(chat_id=update.effective_chat.id, text="Please provide Pollname.")
        return
    poll_id_ = update['message']['text'].split(' ')[1]  # OUR POLL_ID
    description = app.db.session.query(app.Questions).filter_by(poll_id=poll_id_).first().description
    # x = json.load(description)
    jsonData = json.loads(description)
    # print(jsonData)
    params = []  # params[0] = question , rest answers
    for key in jsonData:
        params.append(jsonData[key])
    poll_question = params[0]
    answers = params[1:]
    message = context.bot.send_poll(
        update.effective_chat.id,
        poll_question,
        answers,
        is_anonymous=False,
        allows_multiple_answers=True,
        type=Poll.REGULAR,
        is_closed= False,
        disable_notification= False,
        api_kwargs = {}  #  use either this or poll_id
    )
    # print(message)  # add telegram_id here
    telegram_id = message.poll.id
    app.db.session.query(app.Polls) \
        .filter(app.Polls.poll_id == poll_id_) \
        .update({app.Questions.telegram_question_id: telegram_id})
    app.db.session.commit()


def receive_poll_answer(update: Update, context: CallbackContext) -> None:
    """Summarize a users poll vote"""
    # print("answer update:" ,update)
    answer = update.poll_answer
    print(answer)
    poll_telegram = answer.poll_id
    selected_options = answer.option_ids   # indexes of the selected options
    description = app.db.session.query(app.Questions).filter_by(telegram_question_id=poll_telegram).first().description
    # description = app.db.session.query(app.Questions).filter_by(poll_id=poll_id).first().description
    jsonData = json.loads(description)
    params = []  # params[0] = question , rest answers
    for key in jsonData:
        params.append(jsonData[key])
    poll_question = params[0]
    answers = params[1:]
    user_answers = []
    for i in selected_options:
        user_answers.append(answers[i])
    chat_id = answer.user.id  # user who answered the poll
    poll_id = app.db.session.query(app.Questions).filter_by(telegram_question_id=poll_telegram).first().poll_id
    app.PollsAnswers.addPollAnswer(chat_id, poll_id, poll_telegram, poll_question, user_answers, app.db)  # tomorrow start from here


    # try:
    #     questions = context.bot_data[poll_id]["questions"]
    # # this means this poll answer update is from an old poll, we can't do our answering then
    # except KeyError:
    #     return
    # selected_options = answer.option_ids
    # answer_string = ""
    # for question_id in selected_options:
    #     if question_id != selected_options[-1]:
    #         answer_string += answers[question_id] + " and "
    #     else:
    #         answer_string += answers[question_id]
    # # context.bot.send_message(
    # #     context.bot_data[poll_id]["chat_id"],
    # #     f"{update.effective_user.mention_html()} feels {answer_string}!",
    # #     parse_mode=ParseMode.HTML,
    # # )
    # print(answer_string)
    # context.bot_data[poll_id]["answers"] += 1
    # # Close poll after three participants voted
    # if context.bot_data[poll_id]["answers"] == 3:
    #     context.bot.stop_poll(
    #         context.bot_data[poll_id]["chat_id"], context.bot_data[poll_id]["message_id"]
    #     )
    #

def start_command(update: Update, context: CallbackContext):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Hello")
    context.bot.send_message(chat_id=update.effective_chat.id, text="Welcome to smart polling" + "Please choose one of the options:" )
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text="/register <user-name>-Register to start" +" answering polls via telegram\n" +"<user-name> in smart polling system\n\n"+
                             "\n" + "/remove <user-name>- To stop getting polls queries\n" + "<user-name> in smart polling system\n\n"
                             + "\n" + "/poll <poll-name>- To initalize poll\n <poll-name> in smart polling system\n\n"
                               +"\n"  +  "/start- Use start anytime to see this menu again")


#####                         #######







def help_command(update: Update, context: CallbackContext):
    pass
    # print('do we need this?')


def unregister_cmd(update: Update, context: CallbackContext):
    print("unregister_cmd = ", update['message']['text'])
    len2 = len(update['message']['text'].split(' '))
    if len2 <= 1:
        context.bot.send_message(chat_id=update.effective_chat.id, text="Please provide your username to unregister.")
        return
    user_to_unregister = update['message']['text'].split(' ')[1]
    chat_id = update['message']['chat']['id']
    # params = {'UserName': user_to_unregister, 'ChatId': chat_id, 'context': context}
    params = {'UserName': user_to_unregister, 'ChatId': chat_id}
    response = requests.get(url='http://127.0.0.1:5000/remove', params=params)
    context.bot.send_message(chat_id=update.effective_chat.id, text=response.text)
    # MAYBE NEED TO SWITCH IP


def register_cmd(update: Update, context: CallbackContext):
    print("register_cmd =", update['message']['text'])
    len2 = len(update['message']['text'].split(' '))
    if len2 <= 1:
        context.bot.send_message(chat_id=update.effective_chat.id, text="Please provide username to register.")
        return
    user_to_unregister = update['message']['text'].split(' ')[1]
    chat_id = update['message']['chat']['id']
    params = {'UserName': user_to_unregister, 'ChatId': chat_id}
    response = requests.get(url='http://127.0.0.1:5000/register', params=params)
    context.bot.send_message(chat_id=update.effective_chat.id, text=response.text)
    # MAYBE NEED TO SWITCH IP


def runbot() -> None:
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    print(TELEGRAM_BOT_TOKEN)
    # updater = Updater(os.environ.get(TELEGRAM_BOT_TOKEN, ''))
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

    dispatcher.add_handler(CommandHandler("remove", unregister_cmd))

    dispatcher.add_handler(CommandHandler("register", register_cmd))

    dispatcher.add_handler(CommandHandler('poll', poll))

    dispatcher.add_handler(PollAnswerHandler(receive_poll_answer))

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()

import json
import os
import app
import requests
import telegram
from telegram import Update, ForceReply
# from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
from app import telegram_chat_id_map
from config import bot_key, flask_PATH

import telegram
from telegram import (
    Poll,
    ParseMode,
    KeyboardButton,
    KeyboardButtonPollType,
    ReplyKeyboardMarkup,
    ReplyKeyboardRemove,
    Update,
    Bot)
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
# def poll(update: Update, context: CallbackContext) -> None:
#     # print("unregister_cmd = ", update['message']['text'])
#     # print("poll update:" ,update)
#     # chat_id = update['message']['chat']['id']
#     # print(chat_id)
#     # len2 = len(update['message']['text'].split(' '))
#     # if len2 <= 1 or len2 > 2:
#     #     context.bot.send_message(chat_id=update.effective_chat.id, text="Please provide Pollname.")
#     #     return
#     # poll_id_ = update['message']['text'].split(' ')[1]  # OUR POLL_ID
#     # description = app.db.session.query(app.Questions).filter_by(poll_id=poll_id_).first().description
#     # # x = json.load(description)
#     # jsonData = json.loads(description)
#     # # print(jsonData)
#     # params = []  # params[0] = question , rest answers
#     # for key in jsonData:
#     #     params.append(jsonData[key])
#     # poll_question = params[0]
#     # answers = params[1:]
#     # message = context.bot.send_poll(
#     #     update.effective_chat.id,
#     #     poll_question,
#     #     answers,
#     #     is_anonymous=False,
#     #     allows_multiple_answers=True,
#     #     type=Poll.REGULAR,
#     #     is_closed= False,
#     #     disable_notification= False,
#     #     api_kwargs = {}  #  use either this or poll_id
#     # )
#     # # print(message)  # add telegram_id here
#     # telegram_id = message.poll.id
#     # app.db.session.query(app.Polls) \
#     #     .filter(app.Polls.poll_id == poll_id_) \
#     #     .update({app.Questions.telegram_question_id: telegram_id})
#     # app.db.session.commit()
#
#     json2 = {"question": "how much money do u  want to make?", "answer1": "1M", "answer2": "500", "answer3": "100B",
#              "filter_answer": "100B"}
#     json1 = {"question":"how much money do u make?" ,"answer1":"10k" , "answer2":"30k","answer3":"fuck off","filter_answer": "fuck off"}
#     # data = {"poll_id": 10 , "answer1": 'technion' , "answer2":'cs' , "answer3": 'compi' , "answer4": '75'}
#     headers_dict = {"Poll_name": "salary"}
#     data = {"question":"how much money do u make?" ,"answer1":"10k" , "answer2":"30k","answer3":"fuck off","filter_answer": "fuck off"}
#     url = 'http://127.0.0.1:5000/newpoll'
#     response = requests.post(url, data ,  headers=headers_dict)
#
#     # params = {"poll_id": 10}
#     # response = requests.get(url='http://127.0.0.1:5000/poll_results', params=params)


def receive_poll_answer(update: Update, context: CallbackContext) -> None:
    """Summarize a users poll vote"""
    # print("answer update:" ,update)
    print("INISDE ANSWER BOT")
    answer = update.poll_answer
    print("answer",answer)

    poll_telegram = answer.poll_id
    print("poll_telegram", poll_telegram)

    selected_options = answer.option_ids   # indexes of the selected options
    print("selected_options", selected_options)
    question_id = app.db.session.query(app.telegram_chat_id_map).filter_by(telegram_bot_id=poll_telegram).first().question_id
    print("question_id", question_id)

    question = app.db.session.query(app.Questions).filter_by(
        question_id=question_id).first().question
    # print("question", question)
    answers = app.db.session.query(app.Questions).filter_by(
        question_id=question_id).first().answers
    answers = answers.split(",")
    # print("answers", answers)
    user_answer = ""
    for i in selected_options:
        # user_answers.append(answers[i])
        user_answer += answers[i]
    # print("user_answer", user_answer)
    expected_answer = app.db.session.query(app.telegram_chat_id_map).filter_by(telegram_bot_id=poll_telegram).first().expected_answer
    chat_id = answer.user.id  # user who answered the poll
    poll_name = app.db.session.query(app.Questions).filter_by(question_id=question_id).first().poll_name
    poll_id = app.db.session.query(app.Polls).filter_by(poll_name=poll_name).first().poll_id
    # print("poll_id", poll_id)
    app.PollsAnswers.addPollAnswer(chat_id, poll_id, poll_telegram, question, user_answer,question_id, app.db)

    #  prepare for next question  in poll
    poll_questions = app.db.session.query(app.Polls).filter_by(poll_id=poll_id).first().poll_questions
    # print("poll_questions", poll_questions)
    poll_questions_ids = poll_questions.split(",")[:-1]
    # print("poll_questions after split", poll_questions_ids)
    last_question_in_the_poll = poll_questions_ids[-1]
    # print("last_question_in_the_poll after split", last_question_in_the_poll)


    is_more_question_to_ask =  last_question_in_the_poll != str(question_id)
    # print("is_more_question_to_ask:" , is_more_question_to_ask)
    is_user_asnwered_right = user_answer == expected_answer
    # print("is_user_asnwered_right:", is_user_asnwered_right)
    is_user_active  = app.db.session.query(app.Users).filter_by(chat_id=chat_id).first().active
    # print("is_user_active:", is_user_active)

    # send next poll
    print("is_more_question_to_ask" ,is_more_question_to_ask)
    print("is_user_asnwered_right", is_user_asnwered_right)
    print("is_user_active", is_user_active)
    if is_more_question_to_ask and  is_user_asnwered_right and is_user_active:
        i = 0
        next_question_id = str(-1)
        for question in poll_questions_ids:
            if question == str(question_id):
                next_question_id = poll_questions_ids[i+1]
            else:
                i = i + 1

        next_question_to_send = app.db.session.query(app.Questions).filter_by(
            question_id=next_question_id).first().question
        next_answers_to_send = app.db.session.query(app.Questions).filter_by(
            question_id=next_question_id).first().answers
        next_answers_to_send = next_answers_to_send.split(",")
        message = context.bot.send_poll(
            chat_id,
            next_question_to_send,
            next_answers_to_send,
            is_anonymous=False,
            allows_multiple_answers=False,
            type=Poll.REGULAR,
            is_closed= False,
            disable_notification= False,
            api_kwargs = {}
        )
        expected_answers = app.db.session.query(app.MapPollIdExpectedAnswers).filter_by(poll_id=poll_id).first().expected_answers
        expected_answers = expected_answers[:-1].split(",")
        next_expected_answer = ""
        # print("expected_answers:",expected_answers)
        # create an iterator object from that iterable
        iter_obj = iter(expected_answers)
        # infinite loop
        while True:
            try:
                answer = next(iter_obj)
                # do something with element
                if answer == expected_answer:
                    next_expected_answer = next(iter_obj)
                    break
            except StopIteration:
                # if StopIteration is raised, break from loop
                break
        telegram_chat_id_map.add_new_map(str(message.poll.id), str(chat_id), int(next_question_id),
                                         next_expected_answer, app.db)


def start_command(update: Update, context: CallbackContext):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Hello")
    context.bot.send_message(chat_id=update.effective_chat.id, text="Welcome to smart polling" + "Please choose one of the options:" )
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text="/register <user-name>-Register to start" +" answering polls via telegram\n" +"<user-name> in smart polling system\n\n"+
                             "\n" + "/remove <user-name>- To stop getting polls queries\n" + "<user-name> in smart polling system\n\n"
                               +"\n"  +  "/start- Use start anytime to see this menu again")


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
    response = requests.get(url=flask_PATH+'/remove', params=params)
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
    # response = requests.get(url='http://127.0.0.1:5000/register', params=params)
    response = requests.get(url=flask_PATH + '/register', params=params)
    context.bot.send_message(chat_id=update.effective_chat.id, text=response.text)
    # MAYBE NEED TO SWITCH IP


def runbot() -> None:
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    # print(TELEGRAM_BOT_TOKEN)
    # updater = Updater(os.environ.get(TELEGRAM_BOT_TOKEN, ''))
    # updater = Updater('5067453157:AAHvdsy2WlAEvaYa8cDb059hhIlDm1evPNc')
    updater = Updater(bot_key)


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

    # dispatcher.add_handler(CommandHandler('poll', poll))

    dispatcher.add_handler(PollAnswerHandler(receive_poll_answer))

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()

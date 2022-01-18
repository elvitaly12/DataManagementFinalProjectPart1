import json

from flask import Flask, request
from flask import Response
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import ForeignKey
from config import password
from config import port
from flask_migrate import Migrate
from flask_marshmallow import Marshmallow
from flask_cors import CORS

import telegram
from telegram import (
    Poll,
    ParseMode,
    KeyboardButton,
    KeyboardButtonPollType,
    ReplyKeyboardMarkup,
    ReplyKeyboardRemove,
    Update,
Bot

)



from flask import current_app, flash, jsonify, make_response, redirect, request, url_for

import rncryptor
app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db_name = "beautipoll_db"
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:' + password + '@localhost:'+port+'/'+db_name
db = SQLAlchemy(app)
migrate = Migrate(app, db, compare_type=True,)
cors = CORS()
cors.init_app(app)
ma = Marshmallow(app)

# FLASK_APP= 'app.py'
# db.create_all()


#### 1/10
bot = telegram.Bot(token='5096133703:AAEWvtF28cFDcbbWrqdkpqcfAMTIf_SLmrY')
def sendpoll_to_users(users,question,answers,question_id,expected_answer):

    # active_chat_id =  db.session.query(Users).filter_by(username=user).all().active
    for user in users:
        chat_id = db.session.query(Questions).filter_by(username=user).first().chat_id

        if db.session.query(Users).filter_by(username=user).first().active == True:
            message = bot.send_poll(
                chat_id,
                question,
                answers,
                is_anonymous=False,
                allows_multiple_answers=True,
                type=Poll.REGULAR,
                is_closed=False,
                disable_notification=False,
                api_kwargs={}  # use either this or poll_id
            )
            telegram_chat_id_map.add_new_map(message.poll.id,chat_id,question_id,expected_answer,db)



def send_first_question_in_poll(question_id,expected_answer):
    # print("inside poll: " ,question_id)
    question = db.session.query(Questions).filter_by(
        question_id=int(question_id)).first().question

    answers = db.session.query(Questions).filter_by(
        question_id=int(question_id)).first().answers
    answers = answers.split(",")
    chat_ids =  db.session.query(Users.chat_id).filter_by(
        active=True).all()
    result_dict = map(lambda q: q._asdict(), chat_ids)
    for user_chat_id in result_dict:
        # print(user_chat_id)
        message = bot.send_poll(
            user_chat_id['chat_id'],
            question,
            answers,
            is_anonymous=False,
            allows_multiple_answers=False,
            type=Poll.REGULAR,
            is_closed=False,
            disable_notification=False,
            api_kwargs={}  # use either this or poll_id
        )
        telegram_bot_id = message.poll.id
        # print("telegram_bot_id:" , telegram_bot_id)
        # print("user_chat_id['chat_id']:", user_chat_id['chat_id'])
        telegram_chat_id_map.add_new_map(str(telegram_bot_id), str(user_chat_id['chat_id']),int(question_id),expected_answer, db)



####


def dict_to_json(question_poll,answers_poll):
    dict_to_json = {"question": question_poll}
    i = 1
    for answer in answers_poll:
        answer_key = "answer" + str(i)
        answers_poll = {answer_key: answer}
        i = i + 1
        dict_to_json.update(answers_poll)

    # dict_to_json.update(answers_poll)

    return  dict_to_json



class Users(db.Model):
    username = db.Column(db.String(30), primary_key=True)
    chat_id = db.Column(db.Integer, nullable=False)
    active = db.Column(db.Boolean, nullable=False)

    def __init__(self, username, chat_id, active):
        self.username = username
        self.chat_id = chat_id
        self.active = active

    def __repr__(self):
        # return '<User %r>' % self.username
        return "<Users(username='{}', chat_id={}, active={})>" \
            .format(self.username, self.chat_id, self.active)


    def DeleteUserName(username,db_input):
        obj = Users\
            .query.filter_by(username=username).first()
         # db_input.session.query(Users).filter_by(username=username).first().delete()
        db.session.delete(obj)
        db.session.commit()





    def GetUserNameByChatId(chat_id,db_input):  # check if we  have more than 1 username per chat_id
        return db_input.session.query(Users).filter_by(chat_id=chat_id).first().username

    def IsUserRegisteredByUsername(user_name_inserted, db_input):
        exists = db_input.session.query(Users).filter_by(username=user_name_inserted).first() is not None
        if exists:
            return True
        else:
            return False

    def IsUserActiveByChatID(chat_id_inserted, db_input):
        return db_input.session.query(Users).filter_by(chat_id=chat_id_inserted).first().active

    def IsUserActiveByUsername(username_inserted, db_input):
        return db_input.session.query(Users).filter_by(username=username_inserted).first().active

    def IsUserRegisteredByChatID(chat_id_inserted, db_input):
        return db_input.session.query(Users).filter_by(chat_id=chat_id_inserted).first() is not None

    def IsUserRegisteredAndActiveByChatID(chat_id_inserted, db_input):
        return db_input.session.query(Users).filter_by(chat_id=chat_id_inserted, active=True).first() is not None

    def RegisterUser(username, chat_id, active, db_input):
        new_user = Users(username, chat_id, active)
        db_input.session.add(new_user)
        db_input.session.commit()

    def UnregisterUser(user_name_inserted, chat_id, db_input):
        if not Users.IsUserRegisteredByUsername(user_name_inserted, db_input):
            # here I know there is no active+same chat_id
            return Response("You can't unregister other users.", status=403)
        if not Users.IsUserRegisteredAndActiveByChatID(chat_id, db_input):
            # here I know there is no active+same chat_id
            return Response("This is username was already unregistered.", status=403)
        name = db_input.session.query(Users).filter_by(chat_id=chat_id, active=True).first().username
        print("UnregisterUser name:", name)
        if name is None:
            return Response('You are not registered.', status=403)
        elif name != user_name_inserted:
            return Response("You can't unregister other users.", status=403)
        else:
            active = Users.IsUserActiveByUsername(user_name_inserted, db_input)
            if not active:
                return Response("This is username was already unregistered.", status=403)

            db_input.session.query(Users) \
                .filter(Users.username == user_name_inserted) \
                .update({Users.active: False})
            db_input.session.commit()
            return Response(user_name_inserted + ' unregistered.', status=200)


class Admins(db.Model):
    username = db.Column(db.String(30), primary_key=True)
    encrypted_data = db.Column(db.String(512), nullable=False)
    # key = db.Column(db.String(512), nullable=False)

    def __init__(self, username, encrypted_data):
        self.username = username
        self.encrypted_data = encrypted_data


    def __repr__(self):
        return "<Admins(username='{}', encrypted_data='{}')>" \
            .format(self.username, self.encrypted_data,)


    def add_admin(username,encrypted_data,db_input):
        new_Admin = Admins(username, encrypted_data)
        db_input.session.add(new_Admin)
        db_input.session.commit()

    def Delete_Admin(username, db_input):
        obj = Admins \
            .query.filter_by(username=username).first()
        print(obj)
        # db_input.session.query(Users).filter_by(username=username).first().delete()
        db_input.session.delete(obj)
        db_input.session.commit()

class AdminsSchema(ma.Schema):
    class Meta:
        fields = ('username','encrypted_data')
admin_schema = AdminsSchema()
admins_schema = AdminsSchema(many=True)

class telegram_chat_id_map(db.Model):
    telegram_bot_id = db.Column(db.String(100), primary_key=True)
    chat_id = db.Column(db.String(100), nullable=False)
    question_id = db.Column(db.Integer(),nullable=True)
    expected_answer = db.Column(db.String(100), nullable=True)

    def __init__(self, telegram_bot_id, chat_id,question_id,expected_answer):
        self.telegram_bot_id = telegram_bot_id
        self.chat_id = chat_id
        self.question_id=question_id
        self.expected_answer = expected_answer

    def __repr__(self):
        return "<telegram_chat_id_map(telegram_bot_id='{}', chat_id='{}',question_id={},expected_answer='{}')>" \
            .format(self.telegram_bot_id, self.chat_id,self.question_id,self.expected_answer)


    def add_new_map(telegram_bot_id,chat_id,question_id,expected_answer,db_input):
        new_poll = telegram_chat_id_map(telegram_bot_id,chat_id,question_id,expected_answer)
        db_input.session.add(new_poll)
        db_input.session.commit()

    def DeleteUserName(teelgram_bot_id, db_input):
            print(teelgram_bot_id)
            obj = telegram_chat_id_map \
                .query.filter_by(telegram_bot_id=teelgram_bot_id).first()
            print(obj)
            # db_input.session.query(Users).filter_by(username=username).first().delete()
            db_input.session.delete(obj)
            db_input.session.commit()



class MapPollIdExpectedAnswers(db.Model):
    poll_id = db.Column(db.Integer(), primary_key=True)
    expected_answers = db.Column(db.String(100), nullable=True)

    def __init__(self, poll_id, expected_answers):
        self.poll_id = poll_id
        self.expected_answers = expected_answers

    def __repr__(self):
        return "<MapPollIdExpectedAnswers(poll_id={},expected_answers='{}')>" \
            .format(self.poll_id, self.expected_answers)

    def add_new_map_Poll_expected_asnwers(poll_id, expected_answers,db_input):
        new_poll = MapPollIdExpectedAnswers(poll_id, expected_answers)
        db_input.session.add(new_poll)
        db_input.session.commit()


    def Delete_PollMapping(poll_id, db_input):

            obj = MapPollIdExpectedAnswers \
                .query.filter_by(poll_id=poll_id).first()
            print(obj)
            # db_input.session.query(Users).filter_by(username=username).first().delete()
            db_input.session.delete(obj)
            db_input.session.commit()



class Polls(db.Model):
    poll_id = db.Column(db.Integer, primary_key=True)
    poll_name = db.Column(db.String, primary_key=True)
    # poll_name = db.Column(db.String,nullable=False)
    # poll_telegram_id = db.Column(db.Integer, nullable=True)
    poll_questions = db.Column(db.String(300),nullable=True)  # {1,2,12,34,12} #num =question_id
    expected_answers = db.Column(db.String(300), nullable=True)

    def __init__(self,poll_name,poll_questions,expected_answers):
          self.poll_name = poll_name
          self.poll_questions = poll_questions
          self.expected_answers = expected_answers




    def __repr__(self):
        return "<Polls(poll_id={},poll_name='{}' ,poll_questions='{}',expected_answers='{}')>" \
            .format(self.poll_id,self.poll_name ,self.poll_questions,self.expected_answers)


    def addPoll(poll_questions,poll_name,expected_answers,db_input):
        new_poll = Polls(poll_questions,poll_name,expected_answers)
        db_input.session.add(new_poll)
        db_input.session.commit()

class PollsSchema(ma.Schema):
    class Meta:
        fields = ('poll_id','poll_name','poll_questions')
poll_schema =  PollsSchema()
polls_schema =  PollsSchema(many=True)



class Questions(db.Model):
    question_id = db.Column(db.Integer, primary_key=True)
    poll_name = db.Column(db.String, nullable=True)
    question =  db.Column(db.String(300), nullable=False)
    answers =   db.Column(db.String(300), nullable=False)
    telegram_question_id = db.Column(db.String(50), primary_key=False)   # too many chars for integer


    def __init__(self,  poll_name, question,answers,telegram_question_id):

        self.poll_name = poll_name
        self.question = question
        self.answers = answers
        self.telegram_question_id = telegram_question_id

    def __repr__(self):
        return "<Questions(question_id={},poll_name='{}', question='{}',answers='{}', telegram_question_id='{}')>" \
            .format(self.question_id, self.poll_name, self.question,self.answers,self.telegram_question_id)

    def AddPollQuestion( poll_name, question,answers,telegram_question_id, db_input):
        print(poll_name)
        print(question)
        print(answers)
        print(telegram_question_id)
        new_question = Questions(poll_name, question,answers,telegram_question_id)
        db_input.session.add(new_question)
        db_input.session.commit()

    def GetQuestionByPollname(poll_name, db_input):
       return  db_input.session.query(Users).filter_by(poll_name=poll_name).first().description

class QuestionsSchema(ma.Schema):
    class Meta:
        fields = ('question_id', 'poll_name', 'question','answers','telegram_question_id')

question_schema = QuestionsSchema()
questions_schema = QuestionsSchema(many=True)



class Answers(db.Model):
    answer_id = db.Column(db.Integer, primary_key=True)
    telegram_question_id =  db.Column(db.Integer, primary_key=True)
    # question_id = db.Column(db.Integer, ForeignKey('questions.question_id'), nullable=False)
    description = db.Column(db.String(300), nullable=False)

    def __init__(self, answer_id, telegram_question_id, description):
        self.answer_id = answer_id
        self.telegram_question_id = telegram_question_id
        self.description = description

    def __repr__(self):
        return "<Answers(answer_id={}, telegram_question_id={}, description='{}')>" \
            .format(self.answer_id, self.telegram_question_id, self.description)


class PollsAnswers(db.Model):
    chat_id = db.Column(db.Integer, primary_key=True)
    poll_id = db.Column(db.Integer,  primary_key=True)
    telegram_question_id = db.Column(db.String(100),primary_key=True)
    question_id = db.Column(db.Integer, primary_key=False)
    poll_question = db.Column(db.String, nullable=False)
    answers = db.Column(db.String, nullable=False)


    def __init__(self, chat_id, poll_id, telegram_question_id,poll_question ,answers,question_id):
        self.chat_id = chat_id
        self.poll_id = poll_id
        self.telegram_question_id = telegram_question_id
        self.poll_question = poll_question
        self.answers = answers
        self.question_id = question_id

    def __repr__(self):
        return "<PollsAnswers(chat_id={}, poll_id={}, telegram_question_id='{}',poll_question ='{}' ,answers='{}',question_id={})>" \
            .format(self.chat_id, self.poll_id, self.telegram_question_id,self.poll_question ,self.answers,self.question_id)

    def addPollAnswer(chat_id,poll_id,telegram_question_id,poll_question,answers,question_id,db_input):
        new_pollAnswer = PollsAnswers(chat_id,poll_id,telegram_question_id,poll_question,answers,question_id)
        db_input.session.add(new_pollAnswer)
        db_input.session.commit()


@app.errorhandler(404)
def page_not_found(e):
    return '404 Not Found', 404


@app.errorhandler(500)
def internal_error(e):
    print(e)
    return "500 Internal Server Error"


@app.route('/register', methods=['GET', 'POST'])
def register_HTTP_request():
    user_name_inserted = ""
    if request.method == 'GET':
        user_name_inserted = request.args['UserName']
        chat_id_of_typer = request.args['ChatId']
        # context = request.args['context']
        if Users.IsUserRegisteredAndActiveByChatID(chat_id_of_typer, db):
            print("chat id", chat_id_of_typer, "already registered and active (403)")
            return Response("You're already registered from this account.", status=403)
        elif Users.IsUserRegisteredByChatID(chat_id_of_typer, db):
            if db.session.query(Users).filter_by(chat_id=chat_id_of_typer, username=user_name_inserted).first() is not None:
                # change to active=True:
                name = db.session.query(Users).filter_by(chat_id=chat_id_of_typer, username=user_name_inserted).first()
                db.session.query(Users) \
                    .filter(Users.username == user_name_inserted) \
                    .update({Users.active: True})
                db.session.commit()
                print("chat id", chat_id_of_typer, "already registered with this user name so we change it to active.")
                return Response("You have successfully reactivated your old username! Welcome back to Beautipoll :)", status=200)
            else: #insert new username for the same chat id
                try:
                    Users.RegisterUser(user_name_inserted, chat_id_of_typer, True, db)
                    Response("You have successfully registered with a new username! Welcome back to Beautipoll :)",
                             status=200)
                except Exception as e:
                    print("register_HTTP_request error:", e)
                    return Response('Internal Server Error', status=500)
        # context.bot.send_message(chat_id=chat_id_of_typer, text="You're already registered.")
        elif Users.IsUserRegisteredByUsername(user_name_inserted, db):
            print("username ", user_name_inserted, " already exists(403)")
            return Response('This username is already registered. Please try again with another username.', status=403)
            # request.args['context'].bot.send_message(
            #     chat_id=chat_id_of_typer,
            #     text="This username is already registered. Please try again with another username.")
        else:
            try:
                Users.RegisterUser(user_name_inserted, chat_id_of_typer, True, db)
            except Exception as e:
                print("register_HTTP_request error:", e)
                return Response('Internal Server Error', status=500)
        return Response("You have successfully registered! Welcome to Beautipoll :)", status=200)

    # request.args['context'].bot.send_message(
    #     chat_id=chat_id_of_typer,
    #     text="You have successfully registered! Welcome to Beautipoll :)")

    # error = None
    # if request.method == 'GET':
    #     if request.form['username'] != 'admin' or request.form['password'] != 'admin':
    #         error = 'Invalid Credentials. Please try again.'
    #     else:
    #          return redirect(url_for('home'))
    #          return render_template('login.html', error=error)


@app.route('/remove', methods=['GET', 'POST'])
def unregister_HTTP_request():
    if request.method == 'GET':
        username_unregistered = request.args['UserName']
        typer_chat_id = request.args['ChatId']
        return Users.UnregisterUser(username_unregistered, typer_chat_id, db)

    # error = None
    # if request.method == 'GET':
    #     if request.form['username'] != 'admin' or request.form['password'] != 'admin':
    #         error = 'Invalid Credentials. Please try again.'
    #     else:
    #          return redirect(url_for('home'))
    #          return render_template('login.html', error=error)



@app.route('/activate_poll', methods=['GET', 'POST']) # from ui recieve post request , params like this : headers : poll_name : "fds" , body:{question:"how are you" , answer1:".."}
# previous expected  {poll_id,expected_answers}
def activate_poll():
        try:
            print("are we here? activate_poll")
            poll_name = request.headers.get('poll_name')
            poll_questions = db.session.query(Polls).filter_by(
                poll_name=poll_name).first().poll_questions  # {1,32,545,323,543}
            poll_id = db.session.query(Polls).filter_by(
                poll_name=poll_name).first().poll_id  # {1,32,545,323,543}

            expected_answers = db.session.query(Polls).filter_by(
                poll_name=poll_name).first().expected_answers  # {1,32,545,323,543}
            expected_answers = expected_answers.split(",")
            poll_questions = poll_questions[2:-2]
            question_ids = poll_questions.split(",")
            send_first_question_in_poll(question_ids[0], expected_answers[0])

            expected_Answers = ""
            for answer in expected_answers:
                expected_Answers += answer + ","

            poll_id_in_map = db.session.query(MapPollIdExpectedAnswers).filter_by(poll_id=poll_id).first()
            if poll_id_in_map == None:
                MapPollIdExpectedAnswers.add_new_map_Poll_expected_asnwers(poll_id, expected_Answers, db)
            return Response('OK', status=200)
        except:
            return Response('Internal Error', status=500)




@app.route('/newpoll', methods=['GET', 'POST']) # from ui recieve post request , params like this : headers : poll_name : "fds" , body:{question:"how are you" , answer1:".."}
# previous expected  {poll_id,expected_answers}
def newpoll():


    poll_name = request.headers.get('poll_name')
    # check_if_poll_exists = db.session.query(Polls).filter_by(poll_name=poll_name).first()
    # if check_if_poll_exists != None:
    #     return Response("poll name:" + poll_name + "already exists , please choose different name", status=409)


    # print("poll_name", poll_name)
    # body = request.form
    body = request.headers.get('body')


    poll_question_id  = ""
    expected_answers = ""
    body = body[2:-2]
    # print("body",body)
    body_after_split = body.split(",")


    answers = ""
    answer3a = ""
    answer4a = ""
    filter_answer = "-1"


    try:

        dict = {}
        for iter  in body_after_split:
            iter = iter.replace("{", "")
            iter = iter.replace("}", "")
            key = iter.split(":")[0][1:-1]
            if key == 'answers_counter':
                value = iter.split(":")[1]
            else:
                value = iter.split(":")[1][1:-1]

            dict[key] = value

            if key == 'filter_answer':
                filter_answer = value

            if key == 'answers_counter':

                if value == "2":
                    answers += dict['answer1']+","+dict['answer2']
                    if filter_answer == "1":
                        expected_answers += dict['answer1'] + ","
                    elif filter_answer == "2":
                        expected_answers += dict['answer2'] + ","

                elif value == "3":
                    answers += dict['answer1'] + "," + dict['answer2'] + "," + dict['answer3']
                    if filter_answer == "1":
                        expected_answers += dict['answer1'] + ","
                    elif filter_answer == "2":
                        expected_answers += dict['answer2'] + ","
                    elif filter_answer == "3":
                        expected_answers += dict['answer3'] + ","
                elif value == "4":
                    # print(dict['answer1'])
                    # print(dict['answer2'])
                    # print(dict['answer3'])
                    # print(dict['answer4'])

                    answers += dict['answer1'] + "," + dict['answer2'] + "," + dict['answer3']+"," +dict['answer4']
                    if filter_answer == "1":
                        expected_answers += dict['answer1'] + ","
                    elif filter_answer == "2":
                        expected_answers += dict['answer2'] + ","
                    elif filter_answer == "3":
                        expected_answers += dict['answer3'] + ","
                    elif filter_answer == "4":
                        expected_answers += dict['answer4'] + ","
                Questions.AddPollQuestion(poll_name, dict['question'], answers, "will_changed", db)
                question_id = db.session.query(Questions).filter_by(poll_name=poll_name,
                                                                    question=dict['question']).first().question_id
                poll_question_id += str(question_id) + ","
                answers =""


        Polls.addPoll(poll_name,poll_question_id,expected_answers,db)
        return Response('OK', status=200)

    except Exception as e:
        print(e)
        return Response('Internal Error', status=500)













@app.route('/add_admin', methods=['GET', 'POST'])
def register_new_admin():
    if request.method == 'GET':
        admin_user_name = request.headers.get('Username')
        print('admin_user_name', admin_user_name)
        admin_password = request.headers.get('Password')
        print('admin_password', admin_password)

        check_user_admin = db.session.query(Admins).filter_by(username=admin_user_name).first()
        if check_user_admin is None:
            cryptor = rncryptor.RNCryptor()
            encrypted_data = cryptor.encrypt(admin_password, admin_user_name)
            decoded_data = encrypted_data.decode(encoding= 'iso8859-1')
            Admins.add_admin(admin_user_name, decoded_data,db)
            # salt_from_storage = storage[:32]  # 32 is the length of the salt
            # key_from_storage = storage[32:]

            return Response('OK', status=200)
        else:
            print(409)
            return Response('Conflict', status=409)

@app.route("/login_auth", methods=["GET"], strict_slashes=False)
def login_auth():
    admin_user_name = request.headers.get('Username')

    input_password = request.headers.get('Password')

    admin_entry = db.session.query(Admins).filter_by(
        username=admin_user_name).first()
    # print('admin_entry', admin_entry)

    if not admin_entry:
        # print(401)
        return Response('Unauthorized', status=401)

    else:
        cryptor = rncryptor.RNCryptor()
        encrypted_data = admin_entry.encrypted_data
        encoded_data = encrypted_data.encode(encoding= 'iso8859-1')
        decrypted_data = cryptor.decrypt(encoded_data, admin_user_name)

        if decrypted_data == input_password:
            # print(200)
            return Response('OK', status=200)
        else:
            # print(403)
            return Response('Conflict', status=409)







@app.route('/poll_questions', methods=['GET', 'POST']) # from ui recieve  poll_name return all question
def poll_questions():
    Poll_name = request.headers.get('poll_name')
    my_dict = dict()
    entry = db.session.query(Polls.poll_questions).filter_by(poll_name=Poll_name).first()
    poll_questions = entry.poll_questions.split(",")
    # print('poll_questions_ids: ', poll_questions)
    question_names = []
    poll_questions = poll_questions[:-1]
    # print('poll_questions_ids: ', poll_questions)

    for question_id in poll_questions:
        question_name = db.session.query(Questions).filter_by(question_id=question_id).first().question
        # print('question_name', question_name)
        question_names.append(question_name)
    # print('question_names', question_names)
    # result = questions_schema.dump(question_names)
    # print(result)
    # print("jsonify:", jsonify(question_names))
    return jsonify(question_names)
    # poll_questions = db.session.query(Polls).filter_by(poll_name=Poll_name).first().poll_questions
    # poll_questions =poll_questions[2:-3].split(',')
    # for index, value in enumerate(poll_questions):
    #     description = db.session.query(Questions).filter_by(
    #         question_id=int(value)).first().description
    #
    #     # print("description:" , description)
    #     jsonData = json.loads(description)
    #     params = []  # params[0] = question , rest answers
    #     for key in jsonData:
    #         params.append(jsonData[key])
    #     poll_question = params[0]
    #     my_dict[index] = poll_question
    # # print('my_dict' ,my_dict)


@app.route('/get_Question_send_answer', methods=['GET', 'POST'])  # from ui recieve question_name and poll_name return all answers
def get_Question_send_answer():
    Question_name = request.headers.get('Question_name')
    poll_name = request.headers.get('Poll_name')
    results = []
    question_result = ""
    my_dict = dict()
    answers = db.session.query(Questions).filter_by(
        question=Question_name , poll_name=poll_name).first().answers

    answers_parsed = []
    for key in answers:
        answers_parsed.append(answers[key])
    for answer in answers_parsed:
       answer_count= db.session.query(PollsAnswers.answers).filter_by(answers=answer).count()
       my_dict[answer] = answer_count
    print(my_dict)
    return jsonify(my_dict)




@app.route('/get_admins', methods=['GET', 'POST']) #
def get_admins():
    admins_user_name = db.session.query(Admins.username).all()
    result = admins_schema.dump(admins_user_name)
    # print(result)
    # print("jsonify:", jsonify(result))
    return jsonify(result)


@app.route('/get_pools', methods=['GET', 'POST']) #
def get_polls():
    polls = db.session.query(Polls.poll_name).all()
    result = polls_schema.dump(polls)
    return jsonify(result)



@app.route('/is_poll_exists', methods=['GET', 'POST']) #
def is_poll_exists():
    try:
        poll_name = request.headers.get('poll_name')
        check_if_poll_exists = db.session.query(Polls).filter_by(poll_name=poll_name).first()
    except :
        return Response("internal error", status=500)

    if check_if_poll_exists != None:
        return Response("poll name:" + poll_name + "already exists , please choose different name", status=409)
    else:
        return Response("OK",status=200)


@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'


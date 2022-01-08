import json

from flask import Flask, request
from flask import Response
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import ForeignKey
from config import password
from config import port

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db_name = "beautipoll_db"
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:' + password + '@localhost:'+port+'/'+db_name
db = SQLAlchemy(app)
# db.create_all()





def dict_to_json(question_poll,answers_poll):
    dict_to_json = {"question": question_poll}
    i = 1
    for answer in answers_poll:
        answer_key = "answer" + str(i)
        answers_poll = {answer_key: answer}
        i = i + 1
        dict_to_json.update(answers_poll)

    # dict_to_json.update(answers_poll)
    print(dict_to_json)
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
    password = db.Column(db.String(20), nullable=False)

    def __init__(self, username, password):
        self.username = username
        self.password = password

    def __repr__(self):
        return "<Admins(username='{}', password='{}')>" \
            .format(self.username, self.password)


class Polls(db.Model):
    poll_id = db.Column(db.Integer, primary_key=True)
    # poll_name = db.Column(db.String,nullable=False)
    poll_telegram_id = db.Column(db.Integer, nullable=True)

    def __init__(self, poll_id,poll_telegram_id):
         self.poll_id = poll_id
         self.poll_telegram_id = poll_telegram_id


    def __repr__(self):
        return "<Polls(poll_id={}, poll_telegram_id={})>" \
            .format(self.poll_id, self.poll_telegram_id)


    def addPoll(self,poll_id,poll_telegram,db_input):
        new_poll = Polls(poll_id,poll_telegram)
        db_input.session.add(new_poll)
        db_input.session.commit()



class Questions(db.Model):
    question_id = db.Column(db.Integer, primary_key=True)
    poll_id = db.Column(db.Integer, ForeignKey('polls.poll_id'), nullable=False)
    # description = db.Column(db.String(300), nullable=False)
    description = db.Column(db.JSON(300), nullable=False)


    def __init__(self, question_id, poll_id, description):
        self.question_id = question_id
        self.poll_id = poll_id
        self.description = description

    def __repr__(self):
        return "<Questions(question_id={}, poll_id={}, description='{}')>" \
            .format(self.question_id, self.poll_id, self.description)

    def AddPollQuestion(self,question_id, poll_id, description, db_input):
        new_question = Questions(question_id, poll_id, description)
        db_input.session.add(new_question)
        db_input.session.commit()

    def GetQuestionByPollId(poll_id_, db_input):
       return  db_input.session.query(Users).filter_by(poll_id=poll_id_).first().description





class Answers(db.Model):
    answer_id = db.Column(db.Integer, primary_key=True)
    question_id = db.Column(db.Integer, ForeignKey('questions.question_id'), nullable=False)
    description = db.Column(db.String(300), nullable=False)

    def __init__(self, answer_id, question_id, description):
        self.answer_id = answer_id
        self.question_id = question_id
        self.description = description

    def __repr__(self):
        return "<Answers(answer_id={}, question_id={}, description='{}')>" \
            .format(self.answer_id, self.question_id, self.description)


class PollsAnswers(db.Model):
    username = db.Column(db.String(30), ForeignKey('users.username'), primary_key=True)
    poll_id = db.Column(db.Integer, ForeignKey('polls.poll_id'), primary_key=True)
    question_id = db.Column(db.Integer, ForeignKey('questions.question_id'), primary_key=True)
    answer_id = db.Column(db.Integer, ForeignKey('answers.answer_id'), primary_key=True)

    def __init__(self, username, poll_id, question_id, answer_id):
        self.username = username
        self.poll_id = poll_id
        self.question_id = question_id
        self.answer_id = answer_id

    def __repr__(self):
        return "<PollsAnswers(username='{}', poll_id={}, question_id={}, answer_id={})>" \
            .format(self.username, self.poll_id, self.question_id, self.answer_id)

    def addPollAnswer(self,username,poll_id,question_id,answer_id,db_input):
        new_pollAnswer = PollsAnswers(username,poll_id,question_id,answer_id)
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


# @app.route('/poll', methods=['GET', 'POST'])
# def Set_Poll():
#     poll_id = request.args['poll_id']  # maybe change this to poll_name later
#     description =  db.session.query(Questions).filter_by(poll_id=poll_id).first().description
#     params = [] # params[0] = question , rest answers
#     for key in description:
#         params.append(list[key])






@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'


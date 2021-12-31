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

    def IsUserRegisteredByUsername(user_name_inserted, db):
        exists = db.session.query(Users).filter_by(username=user_name_inserted).first() is not None
        if exists:
            return True
        else:
            return False

    def IsUserRegisteredByChatID(chat_id_inserted, db):
        exists = db.session.query(Users).filter_by(chat_id=chat_id_inserted).first() is not None
        if exists:
            return True
        else:
            return False

    def RegisterUser(username, chat_id, active, db):
        newuser = Users(username, chat_id, active)
        db.session.add(newuser)
        db.session.commit()

    def UnregisterUser(user_name_inserted, chat_id, db):
        name = db.session.query(Users).filter_by(chat_id=chat_id).first().username
        print("UnregisterUser name:", name)
        if name is None:
            return Response('Internal Server Error', status=500)
        elif name != user_name_inserted:
            return Response("You can't unregister other users.", status=403)
        else:
            db.session.query(Users) \
                .filter(Users.username == user_name_inserted) \
                .update({Users.active: False})
            db.session.commit()
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

    def __init__(self, poll_id):
        self.poll_id = poll_id

    def __repr__(self):
        return "<Polls(poll_id={})>" \
            .format(self.poll_id)


class Questions(db.Model):
    question_id = db.Column(db.Integer, primary_key=True)
    poll_id = db.Column(db.Integer, ForeignKey('polls.poll_id'), nullable=False)
    description = db.Column(db.String(300), nullable=False)

    def __init__(self, question_id, poll_id, description):
        self.question_id = question_id
        self.poll_id = poll_id
        self.description = description

    def __repr__(self):
        return "<Questions(question_id={}, poll_id={}, description='{}')>" \
            .format(self.question_id, self.poll_id, self.description)


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


@app.errorhandler(404)
def page_not_found(e):
    return '404 Not Found', 404


@app.errorhandler(500)
def internal_error(e):
    print(e)
    return "500 Error"


@app.route('/register', methods=['GET', 'POST'])
def register_HTTP_request():
    user_name_inserted = ""

    if request.method == 'GET':
        user_name_inserted = request.args['UserName']
        chat_id_of_typer = request.args['ChatId']
        # context = request.args['context']
        if Users.IsUserRegisteredByChatID(chat_id_of_typer, db):
            print("chat id", chat_id_of_typer, "already registered (403)")
            return Response("You're already registered from this account.", status=403)
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
    # request.args['context'].bot.send_message(
    #     chat_id=chat_id_of_typer,
    #     text="You have successfully registered! Welcome to Beautipoll :)")
    return Response("You have successfully registered! Welcome to Beautipoll :)", status=200)

    # error = None
    # if request.method == 'GET':
    #     if request.form['username'] != 'admin' or request.form['password'] != 'admin':
    #         error = 'Invalid Credentials. Please try again.'
    #     else:
    #          return redirect(url_for('home'))
    #          return render_template('login.html', error=error)


@app.route('/unregister', methods=['GET', 'POST'])
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


@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'


from flask import Flask, redirect, url_for, abort, request, render_template
from flask import Response
import DatabaseLogic as DB
from werkzeug.debug import get_current_traceback
from sqlalchemy.ext.declarative import declarative_base
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, Date, Boolean, ForeignKey

import logging

from passwordfile import password

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:' + password + '@localhost:5434/postgres'
db = SQLAlchemy(app)





# def init_db():



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

    def Check_User_Registered_By_Username(user_name_inserted, db):
        exists = db.session.query(Users).filter_by(username=user_name_inserted).first() is not None
        print(exists)
        if exists:
            return True
        else:
            return False

    def Check_User_Registered_By_ChatID(chat_id_inserted, db):
        exists = db.session.query(Users).filter_by(chat_id=chat_id_inserted).first() is not None
        # print(exists)
        if exists:
            return True
        else:
            return False

    def Register_NewUser(username, chat_id, active, db):
        newuser = Users(username, chat_id, active)
        db.session.add(newuser)
        db.session.commit()

    def User_UnRegister(user_name_inserted, chat_id, db):
        name = db.session.query(Users).filter_by(chat_id=chat_id).first().username
        print(name)
        if name is None:
            return Response('Internal Server Error', status=500)
        elif name != user_name_inserted:
            return Response('Access denied, cant unregister other user', status=500)
        else:
            db.session.query(Users) \
                .filter(Users.username == user_name_inserted) \
                .update({Users.active: False})
            db.session.commit()
            return Response(user_name_inserted + ' unregistered', status=200)


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
def register():
    user_name_inserted = ""
    # error = None
    # if request.method == 'GET':
    #     if request.form['username'] != 'admin' or request.form['password'] != 'admin':
    #         error = 'Invalid Credentials. Please try again.'
    #     else:
    #          return redirect(url_for('home'))
    #          return render_template('login.html', error=error)

    if request.method == 'GET':
       user_name_inserted = request.args['UserName']
       chat_id_of_typer =  request.args['ChatId']
       if Users.Check_User_Registered_By_ChatID(chat_id_of_typer,db):
           Response('chat id already exists', status=403)
           print("chat id ", chat_id_of_typer, " already exists(403)")
       elif Users.Check_User_Registered_By_Username(user_name_inserted,db):
           Response('username already exists', status=403)
           print("username ", user_name_inserted, " already exists(403)")
       else:
           try:
               Users.Register_NewUser(user_name_inserted, chat_id_of_typer,True,db)
           except Exception:
               Response('Internal Server Error', status=500)
               print("inside exception(register)")



    return Response(user_name_inserted +' registered', status=200)


@app.route('/unregister', methods=['GET', 'POST'])
def unregister():
    print('are we herhe???')
    user_name_uninserted=""
    # error = None
    # if request.method == 'GET':
    #     if request.form['username'] != 'admin' or request.form['password'] != 'admin':
    #         error = 'Invalid Credentials. Please try again.'
    #     else:
    #          return redirect(url_for('home'))
    #          return render_template('login.html', error=error)

    if request.method == 'GET':
        user_name_uninserted = request.args['UserName']
        chat_id_of_typer = request.args['ChatId']
        return Users.User_UnRegister(user_name_uninserted, chat_id_of_typer, db)








@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'


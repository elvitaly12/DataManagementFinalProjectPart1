from sqlalchemy.dialects.postgresql import psycopg2

import config
from DatabaseLogic import createDB
from bot_logic import runbot
from server_logic import app

from passwordfile import password

import threading
import sqlalchemy
from sqlalchemy import create_engine, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, Date, Boolean
Base = declarative_base()
from flask import Flask

db = SQLAlchemy(app)


class FlaskThread(threading.Thread):
    def run(self) -> None:
        app.run()


class TelegramThread(threading.Thread):
    def run(self) -> None:
        runbot()

# class DBThread(threading.Thread):
#     def run(self) -> None:
#
#         createDB()


class Users(db.Model):
    username = db.Column(db.String(30), primary_key=True)
    active = db.Column(db.Boolean, nullable=False)
    chat_id = db.Column(db.Integer, nullable=False)

    def __init__(self, username, active, chat_id):
        self.username = username
        self.active = active
        self.chat_id = chat_id

    def __repr__(self):
        # return '<User %r>' % self.username
        return "<Users(username='{}', active={}, chat_id={})>" \
            .format(self.username, self.active, self.chat_id)


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
    poll_id = db.Column(db.Integer, ForeignKey('Polls.poll_id'), nullable=False)
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
    question_id = db.Column(db.Integer, ForeignKey('Questions.question_id'), nullable=False)
    description = db.Column(db.String(300), nullable=False)

    def __init__(self, answer_id, question_id, description):
        self.answer_id = answer_id
        self.question_id = question_id
        self.description = description

    def __repr__(self):
        return "<Answers(answer_id={}, question_id={}, description='{}')>" \
            .format(self.answer_id, self.question_id, self.description)


class PollsAnswers(db.Model):
    username = db.Column(db.String(30), ForeignKey('Users.username'), primary_key=True)
    poll_id = db.Column(db.Integer, ForeignKey('Polls.poll_id'), primary_key=True)
    question_id = db.Column(db.Integer, ForeignKey('Questions.question_id'), primary_key=True)
    answer_id = db.Column(db.Integer, ForeignKey('Answers.answer_id'), primary_key=True)

    def __init__(self, username, poll_id, question_id, answer_id):
        self.username = username
        self.poll_id = poll_id
        self.question_id = question_id
        self.answer_id = answer_id

    def __repr__(self):
        return "<PollsAnswers(username='{}', poll_id={}, question_id={}, answer_id={})>" \
            .format(self.username, self.poll_id, self.question_id, self.answer_id)


if __name__ == "__main__":
    # app = Flask(__name__)
    # app.run()
    # app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://postgres:q1w2e3r4t@localhost:5433/books"
    # engine = create_engine(app.config["SQLALCHEMY_DATABASE_URI"])
    # Base.metadata.create_all(engine)

    app = Flask(__name__)
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:'+password+'@localhost:5433/postgres'


    db.create_all()
    db.session.commit()
    admin = Users('admin', 'admin@example.com')
    guest = Users('guest', 'guest@example.com')
    db.session.add(admin)
    db.session.add(guest)
    db.session.commit()
    users = Users.query.all()
    print(users)




    # bamba1 = BAMBA('1', 'admin@example.com')
    # bamba2 = User('2', 'guest@example.com')
    # db.session.add(bamba1)
    # db.session.add(bamba2)
    # db.session.commit()
    # users = User.query.all()
    #
    #
    #
    # print(users)


    # db = SQLAlchemy(app)
    # db.create_all()


    # # createDB()
    # flask_thread = FlaskThread()
    # flask_thread.start()
    # bot_thread = TelegramThread()
    # bot_thread.start()
    # # db_thread = DBThread()
    # # db_thread.start()
    # # runbot()

    # main()
from sqlalchemy.dialects.postgresql import psycopg2

import config
from DatabaseLogic import createDB
from bot_logic import runbot
from server_logic import app

from passwordfie import password

import threading
import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date
Base = declarative_base()
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

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

class Book(Base):
    __tablename__ = 'books'
    id = Column(Integer, primary_key=True)
    title = Column(String)
    author = Column(String)
    pages = Column(Integer)
    published = Column(Date)

    def __repr__(self):
        return "<Book(title='{}', author='{}', pages={}, published={})>" \
            .format(self.title, self.author, self.pages, self.published)
if __name__ == "__main__":
    # app = Flask(__name__)
    # app.run()
    # app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://postgres:q1w2e3r4t@localhost:5433/books"
    # engine = create_engine(app.config["SQLALCHEMY_DATABASE_URI"])
    # Base.metadata.create_all(engine)

    app = Flask(__name__)
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:123456@localhost:5433/postgres'
    db = SQLAlchemy(app)
    class User(db.Model):
        id = db.Column(db.Integer, primary_key=True)
        username = db.Column(db.String(80), unique=True)
        email = db.Column(db.String(120), unique=True)

        def __init__(self, username, email):
            self.username = username
            self.email = email

        def __repr__(self):
            return '<User %r>' % self.username

    class BAMBA(db.Model):
        id = db.Column(db.Integer, primary_key=True)
        bamba1 = db.Column(db.String(80), unique=True)
        bamba2 = db.Column(db.String(120), unique=True)

        def __init__(self, username, email):
            self.username = username
            self.email = email

        def __repr__(self):
            return '<BAMBA %r>' % self.username

    db.create_all()
    db.session.commit()
    admin = User('admin', 'admin@example.com')
    guest = User('guest', 'guest@example.com')
    db.session.add(admin)
    db.session.add(guest)
    db.session.commit()
    users = User.query.all()
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
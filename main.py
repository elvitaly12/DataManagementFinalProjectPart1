from sqlalchemy.dialects.postgresql import psycopg2

import config

from DatabaseLogic import createDB
from bot_logic import runbot
from server_logic import app

from passwordfile import password

import threading
import sqlalchemy
from sqlalchemy import create_engine, ForeignKey, false
from sqlalchemy.ext.declarative import declarative_base
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, Date, Boolean
Base = declarative_base()
from flask import Flask


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




# def init_db():
    # app = Flask(__name__)
    # app.run()
    # app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://postgres:q1w2e3r4t@localhost:5433/books"
    # engine = create_engine(app.config["SQLALCHEMY_DATABASE_URI"])
    # Base.metadata.create_all(engine)


if __name__ == "__main__":
    flask_thread = FlaskThread()
    flask_thread.start()
    bot_thread = TelegramThread()
    bot_thread.start()


















    # main()
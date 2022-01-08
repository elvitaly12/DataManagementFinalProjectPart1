import json
import os
import operator

from sqlalchemy_utils.aggregates import manager

from bot_logic import runbot
from server_logic import app, dict_to_json, Questions, Polls
import threading
from sqlalchemy.ext.declarative import declarative_base
from server_logic import db
from sqlalchemy_utils import database_exists, create_database
# Base = declarative_base()
# # from flask.ext.migrate import Migrate, MigrateCommand
# from flask_migrate import Migrate,MigrateCommand
from flask.cli  import FlaskGroup






class FlaskThread(threading.Thread):
    def run(self) -> None:
        if not database_exists(app.config['SQLALCHEMY_DATABASE_URI']):
            print("db doesn't exists. creating db:")
            create_database(app.config['SQLALCHEMY_DATABASE_URI'])
            db.create_all()
        else:
            print("db exists")
        app.run()

class TelegramThread(threading.Thread):
    def run(self) -> None:
        runbot()

# class DBThread(threading.Thread):
#     def run(self) -> None:
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
    # bot_thread = TelegramThread()
    # bot_thread.start()
    cli = FlaskGroup(app)







    # poll = Polls(10,-1)
    # poll.addPoll(10,-1,db)  # tomorrow start from here
    # question_id = 1
    # poll_id = 2
    # question = "how are you"
    # answers = ["good", "great", "bad"]
    # json_object = dict_to_json(question, answers)
    #
    # tmp = Questions(question_id,poll_id,json_object)
    # tmp.AddPollQuestion(question_id,poll_id,json_object,db)




















    # main()
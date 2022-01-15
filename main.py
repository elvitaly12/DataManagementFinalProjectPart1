import json
import os
import operator
from sqlalchemy_utils.aggregates import manager

from bot_logic import runbot
from app import app,Users, dict_to_json, Questions, Polls,telegram_chat_id_map,MapPollIdExpectedAnswers,PollsAnswers
import threading
from sqlalchemy.ext.declarative import declarative_base
from app import db
from sqlalchemy_utils import database_exists, create_database
# Base = declarative_base()
# # from flask.ext.migrate import Migrate, MigrateCommand
# from flask_migrate import Migrate,MigrateCommand
# from flask.cli  import FlaskGroup


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
    bot_thread = TelegramThread()
    bot_thread.start()

    # PollsAnswers.addPollAnswer(1, 10, 1111, "where do u study?", "technion", 11, db)
    # PollsAnswers.addPollAnswer(2, 10, 1112, "where do u study?", "tel-aviv", 11, db)

    # db.session.query(PollsAnswers).delete()
    # db.session.commit()



    # db.session.query(Users.id == 123).delete()
    # db.session.query(Users).filter_by(username="ofir89").first().delete()
    # db.session.commit()

    # telegram_chat_id_map.DeleteUserName("5978536395189256206",db)

    # Polls.addPoll(10,'{11,12,13,14,}',db)
    # description = {"question": "where do u study?",'answer1':"technion",'answer2':"ben-gurion",
    #                'answer3':"tel-aviv",'answer4':"jerusalem"}
    # Questions.AddPollQuestion(11,10,description,-1,db)
    #
    # description = {"question": "which faculty?", 'answer1': "cs", 'answer2': "hasmal",
    #                'answer3': "math", 'answer4': "medicine"}
    # Questions.AddPollQuestion(12, 10, description, -1, db)
    #
    # description = {"question": "which course", 'answer1': "matam", 'answer2': "ds",
    #                'answer3': "os", 'answer4': "compi"}
    # Questions.AddPollQuestion(13, 10, description, -1, db)
    #
    # description = {"question": "grade u want?", 'answer1': "65", 'answer2': "70",
    #                'answer3': "75", 'answer4': "99"}
    # Questions.AddPollQuestion(14, 10, description, -1, db)




















    # main()
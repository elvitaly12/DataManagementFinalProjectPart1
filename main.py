import json
import os
import operator
from sqlalchemy_utils.aggregates import manager

from bot_logic import runbot
from app import app,Users, dict_to_json, Questions, Polls,telegram_chat_id_map,MapPollIdExpectedAnswers,PollsAnswers,Admins
import threading
from sqlalchemy.ext.declarative import declarative_base
from app import db
from sqlalchemy_utils import database_exists, create_database
# Base = declarative_base()
# # from flask.ext.migrate import Migrate, MigrateCommand
# from flask_migrate import Migrate,MigrateCommand
# from flask.cli  import FlaskGroup
import hashlib

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
import rncryptor



if __name__ == "__main__":

    # # rncryptor.RNCryptor's methods
    # cryptor = rncryptor.RNCryptor()
    # encrypted_data = cryptor.encrypt(password, username)
    # encoded_data = encrypted_data.decode(encoding= 'iso8859-1')
    # # Admins.Delete_Admin("vitaly", db)
    # Admins.add_admin(username,encoded_data,db)

   poll =  [{"question":"test question","answer1":"test ans1","answer2":"test ans2","filter_answer":"1"},{"question":"question2","answer1":"2_answer1","answer2":"3_answer2","answer3":"ans3","answer4":"test ans4","filter_answer":"4"}]#
   for json in poll:
       b_in_dict =  "answer3" in json
       print(b_in_dict)





    # Admins.add_admin(username,encrypted_data)

    # # rncryptor's functions
    # encrypted_data = rncryptor.encrypt(username, password)
    # decrypted_data = rncryptor.decrypt(encrypted_data, password)
    # assert username == decrypted_data
    #
    # flask_thread = FlaskThread()
    # flask_thread.start()
    # bot_thread = TelegramThread()
    # bot_thread.start()

    # Polls.addPoll( "grades", '1,2,3',db)
    # Polls.addPoll("salary", '1,2,3',db)
    # Polls.addPoll("hobbies", '1,2,3',db)
    # Polls.addPoll("games", '1,2,3',db)
    # db.session.commit()











    # salt = db.session.query(Admins).filter_by(
    #     username="vitaly").first().salt
    # # print("salt:", salt)
    #
    # old_key = db.session.query(Admins).filter_by(
    #     username="vitaly").first().key
    # username = "vitaly"
    # password = "123456"
    # salt_test = os.urandom(32)  # for each user , we store differnt salt [:32]
    # str_salt = str(salt_test)





    # PollsAnswers.addPollAnswer(1, 10, 1111, "where do u study?", "technion", 11, db)
    # PollsAnswers.addPollAnswer(2, 10, 1112, "where do u study?", "tel-aviv", 11, db)
    #




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






    # db.session.query(telegram_chat_id_map).delete()
    # db.session.query(MapPollIdExpectedAnswers).delete()
    # db.session.query(PollsAnswers).delete()
    # db.session.query(Questions).delete()
    # db.session.query(Polls).delete()
    # db.session.commit()














    # main()
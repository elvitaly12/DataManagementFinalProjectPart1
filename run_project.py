from bot_logic import runbot
from app import app,Users, dict_to_json, Questions, Polls,telegram_chat_id_map,MapPollIdExpectedAnswers,PollsAnswers,Admins
import threading
import subprocess
from app import db
from sqlalchemy_utils import database_exists, create_database

from config import  super_admin_user,super_admin_password,flask_port
import os

class FlaskThread(threading.Thread):
    def run(self) -> None:
        if not database_exists(app.config['SQLALCHEMY_DATABASE_URI']):
            print("db doesn't exists. creating db:")
            create_database(app.config['SQLALCHEMY_DATABASE_URI'])
            db.create_all()
            Admins.add_superadmin(super_admin_user,super_admin_password)
        else:
            print("db exists")
        app.run(port=flask_port)

class TelegramThread(threading.Thread):
    def run(self) -> None:
        runbot()



class ReactThread(threading.Thread):
    def run(self) -> None:
        os.chdir("./fronted_react")  # change this before submission
        subprocess.check_call('npm install', shell=True)
        subprocess.check_call('npm start', shell=True)










# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    flask_thread = FlaskThread()
    flask_thread.start()
    bot_thread = TelegramThread()
    bot_thread.start()
    react_thread = ReactThread()
    react_thread.start()


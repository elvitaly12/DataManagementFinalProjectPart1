from bot_logic import runbot
from app import app,Users, dict_to_json, Questions, Polls,telegram_chat_id_map,MapPollIdExpectedAnswers,PollsAnswers,Admins
import threading
import subprocess
from app import db
from sqlalchemy_utils import database_exists, create_database ,drop_database
import requests
from config import  super_admin_user,super_admin_password,flask_port,flask_local_host
import os
from multiprocessing import Process
import subprocess
import os


class FlaskThread(threading.Thread):
    def run(self) -> None:
        if not database_exists(app.config['SQLALCHEMY_DATABASE_URI']):
            print("db doesn't exists. creating db:")
            create_database(app.config['SQLALCHEMY_DATABASE_URI'])
            db.create_all()
            Admins.add_superadmin(super_admin_user,super_admin_password,db)
        else:
            print("db exists")
        app.run(host=flask_local_host, port=flask_port)

class TelegramThread(threading.Thread):
    def run(self) -> None:
        runbot()


# class ReactThread(threading.Thread):
# def run(self) -> None:
def runReactProcess():
        os.chdir("./src")  # change this before submission
        subprocess.check_call('npm install', shell=True)
        subprocess.check_call('npm start', shell=True)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    drop_database(app.config['SQLALCHEMY_DATABASE_URI'])
    flask_thread = FlaskThread()
    flask_thread.start()
    bot_thread = TelegramThread()
    bot_thread.start()

    # react_thread = ReactThread()
    # react_thread.start()
    react_process = Process(target=runReactProcess)
    react_process.start()

    # params = {'userName': super_admin_user, 'password': super_admin_password}
    # response = requests.get(url='http://127.0.0.1:5000/add_admin', params=params)
    # db.drop_all()


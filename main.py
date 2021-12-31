from bot_logic import runbot
from server_logic import app
import threading
from sqlalchemy.ext.declarative import declarative_base
from server_logic import db
from sqlalchemy_utils import database_exists, create_database
from sqlalchemy import create_engine
Base = declarative_base()


class FlaskThread(threading.Thread):
    def run(self) -> None:
        # engine = create_engine("postgres://localhost/mydb")
        # if not database_exists(engine.url):
        #     create_database(engine.url)
        if not database_exists(app.config['SQLALCHEMY_DATABASE_URI']):
            print("db doesn't exists. creating db:")
            create_database(app.config['SQLALCHEMY_DATABASE_URI'])
            db.create_all()
        else: print("db exists")
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


















    # main()
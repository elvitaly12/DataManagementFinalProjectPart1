from DatabaseLogic import createDB
from server_logic import app
from bot_logic import runbot
import threading



class FlaskThread(threading.Thread):
    def run(self) -> None:
        app.run()
        # createDB()


class TelegramThread(threading.Thread):
    def run(self) -> None:
        runbot()

# class DBThread(threading.Thread):
#     def run(self) -> None:
#
#         createDB()


if __name__ == "__main__":
    # createDB()
    flask_thread = FlaskThread()
    flask_thread.start()
    bot_thread = TelegramThread()
    bot_thread.start()
    # db_thread = DBThread()
    # db_thread.start()
    # runbot()

    # main()
from server_logic import app
from bot_logic import runbot
import threading



class FlaskThread(threading.Thread):
    def run(self) -> None:
        app.run()


class TelegramThread(threading.Thread):
    def run(self) -> None:
        runbot()


if __name__ == "__main__":
    flask_thread = FlaskThread()
    flask_thread.start()
    bot_thread = TelegramThread()
    bot_thread.start()
    # runbot()

    # main()
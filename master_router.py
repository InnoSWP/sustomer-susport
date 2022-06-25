import logging
import asyncio
import threading

from flask_server.server import FlaskThread
from telegram_server.bot import BotThread


def setup_threads():
    tg_thread = BotThread()
    flask_thread = FlaskThread()

    tg_thread.add_callback(flask_thread.flask_callback)
    flask_thread.add_callback(tg_thread.send_message)

    # Start flask thread
    threading.Thread(target=flask_thread.run).start()

    # asyncio automatically starts loop
    threading.Thread(target=asyncio.run, args=(tg_thread.polling(),))


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        datefmt='%H:%M:%S'
    )

    setup_threads()

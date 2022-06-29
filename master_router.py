import asyncio
import logging
from multiprocessing import Process, Pipe

from flask_server.server import FlaskThread
from telegram_server.bot import BotThread


def setup_threads():
    parent, child = Pipe(duplex=True)

    tg_object = BotThread(child)
    flask_object = FlaskThread(parent)

    # tg_object.add_callback(flask_object.flask_callback)
    # flask_object.add_callback(tg_object.send_message)

    # Start flask thread
    # threading.Thread(target=flask_thread.run).start()
    flask_process = Process(target=flask_object.run, args=())

    # asyncio automatically starts loop
    # threading.Thread(target=asyncio.run, args=(tg_thread.polling(),))
    tg_process = Process(target=asyncio.run, args=(tg_object.run(),))

    flask_process.start()
    tg_process.start()

    flask_process.join()
    tg_process.join()


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        datefmt='%H:%M:%S'
    )
    setup_threads()

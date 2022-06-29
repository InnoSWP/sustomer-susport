import logging
from multiprocessing import Pipe, Process

from flask_server.server import FlaskThread
from telegram_server.bot import BotThread


def setup_threads():
    parent, child = Pipe(duplex=True)

    ts = [BotThread(parent), FlaskThread(child)]
    ps = [Process(target=t.run) for t in ts]

    [p.start() for p in ps]
    [p.join() for p in ps]


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        datefmt='%H:%M:%S'
    )

    setup_threads()

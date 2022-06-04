import asyncio
from time import sleep, time
from typing import Callable

from telegram import Update
from telegram.ext import Application, CallbackContext, MessageHandler, filters

import logging
import functools

def call_decorator(func):
    @functools.wraps(func)
    def inner(*args, **kwargs):
        logging.info(f'{func.__name__}: {args}, {kwargs}')

        return func(*args, **kwargs)

    return inner

class BotThread:
    isAlive: bool = True
    _callbacks: list[Callable] = list()

    def __init__(self, name) -> None:
        self.name = name

    def add_callback(
        self, callback: Callable): self._callbacks.append(callback)

    @call_decorator
    async def send_message(self, update: Update, context: CallbackContext.DEFAULT_TYPE):
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="Text 123"
        )

    def polling(self):
        application = Application.builder().token('5558795989:AAGL-wdNB597fVr-VI-pzTfxeO-WdIA-vAg').build()

        async def handler(*args, **kwargs):
            self._callbacks[0].__call__(*args, **kwargs)

        unknown_handler = MessageHandler(filters.TEXT, handler)
        application.add_handler(unknown_handler)

        application.run_polling()


class FlaskThread:
    _callbacks: list[Callable] = list()
    _dead_callbacks: list[Callable] = list()
    # here add all callbacks for sevices

    def add_callback(
        self, callback: Callable): self._callbacks.append(callback)

    @call_decorator
    def send_some_api_to_front_callback(self, *args, **kwargs):
        pass

    # imagine that here is something good
    def trigger_callbacks(self, msg: str):
        for callback in self._callbacks:
            callback(f'site triggered {msg} bot at {time()}')

    def run(self):
        from random import randint
        for _ in range(2):
            self.trigger_callbacks(str(randint(1, 10000)))
            sleep(0.5)
        print("site is killing bots")
        for dead in self._dead_callbacks:
            dead()
        print("site is dead")


def thread_run():
    import threading

    tg_thread = BotThread("biba")
    flask_thread = FlaskThread()

    tg_thread.add_callback(flask_thread.send_some_api_to_front_callback)

    bot_thread = threading.Thread(target=asyncio.run, args=(tg_thread.polling(),))
    flask_thread = threading.Thread(target=flask_thread.run)

    print("ready to launch")
    bot_thread.start()
    flask_thread.start()

    print("started")
    bot_thread.join()
    flask_thread.join()


if __name__ == "__main__":
    # set up logging to file
    logging.basicConfig(
        level=logging.INFO,
        format='[%(asctime)s] {%(pathname)s:%(lineno)d} %(levelname)s - %(message)s',
        # datefmt='%H:%M:%S'
    )

    thread_run()

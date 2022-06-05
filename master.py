import asyncio
from typing import Callable

import telegram
from telegram import Update
from telegram.ext import Application, CallbackContext, MessageHandler, filters

import logging
from functools import wraps

def call_decorator(func):
    @wraps(func)
    def inner(*args, **kwargs):
        logging.info(f'{func.__name__}: {args}, {kwargs}')

        return func(*args, **kwargs)

    return inner


def run(func):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    loop.run_until_complete(func.__call__())
    loop.close()


class BotThread:
    isAlive: bool = True
    _callbacks: list[Callable] = list()

    def __init__(self, token: str) -> None:
        self._token = token

    def add_callback(self, callback: Callable):
        self._callbacks.append(callback)

    @call_decorator
    async def send_message(self, bot: telegram.Bot, chat_id: int, message_text: str):
        await bot.send_message(
            chat_id=chat_id,
            text=message_text,
        )

    def polling(self):
        application = Application.builder().token(self._token).build()

        # async def handler(*args, **kwargs):
        #     await self._callbacks[0].__call__(*args, **kwargs)

        handler = self._callbacks[0]

        text_handler = MessageHandler(filters.TEXT, handler)
        application.add_handler(text_handler)

        application.run_polling()


class FlaskThread:
    _callbacks: list[Callable] = list()

    def add_callback(self, callback: Callable):
        self._callbacks.append(callback)

    @call_decorator
    async def send_some_api_to_front_callback(self, update: Update, context: CallbackContext.DEFAULT_TYPE):
        chat_id = update.effective_chat.id
        bot = context.bot

        send_message = self._callbacks[0]

        await send_message(bot, chat_id, update.message.text + '123')

    def run(self):
        while True:
            pass  # TODO Flask


def thread_run():
    import threading

    token = '5558795989:AAGL-wdNB597fVr-VI-pzTfxeO-WdIA-vAg'  # TODO manage token

    tg_thread = BotThread(token)
    flask_thread = FlaskThread()

    tg_thread.add_callback(flask_thread.send_some_api_to_front_callback)
    flask_thread.add_callback(tg_thread.send_message)

    bot_thread = threading.Thread(target=asyncio.run, args=(tg_thread.polling(),))  # TODO blocks code below
    flask_thread = threading.Thread(target=flask_thread.run)

    logging.info("ready to launch")
    bot_thread.start()
    flask_thread.start()

    logging.info("started")
    bot_thread.join()
    flask_thread.join()


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format='[%(asctime)s] {%(pathname)s:%(lineno)d} %(levelname)s - %(message)s',
        datefmt='%H:%M:%S'
    )

    thread_run()

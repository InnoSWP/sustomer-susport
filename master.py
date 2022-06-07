import asyncio
import logging
import threading
from typing import Callable

import telegram
from telegram.ext import Application, MessageHandler, filters

from flask_server import FlaskThread
from utils import call_decorator


class BotThread:
    isAlive: bool = True
    _callbacks: list[Callable] = list()

    def __init__(self, token: str) -> None:
        self._token = token
        self.application = None

    def add_callback(self, callback: Callable):
        self._callbacks.append(callback)

    @call_decorator
    async def send_message(self, bot: telegram.Bot, chat_id: int, message_text: str):
        await bot.send_message(
            chat_id=chat_id,
            text=message_text,
        )

    def polling(self):
        self.application = Application.builder().token(self._token).build()

        handler = self._callbacks[0]

        text_handler = MessageHandler(filters.TEXT, handler)
        self.application.add_handler(text_handler)

        self.application.run_polling()


def thread_run():
    token = '5558795989:AAGL-wdNB597fVr-VI-pzTfxeO-WdIA-vAg'  # TODO manage token

    tg_thread = BotThread(token)
    flask_thread = FlaskThread()

    tg_thread.add_callback(flask_thread.send_some_api_to_front_callback)
    flask_thread.add_callback(tg_thread.send_message)

    # Start flask thread
    threading.Thread(target=flask_thread.run).start()

    # asyncio automatically starts loop
    threading.Thread(target=asyncio.run, args=(tg_thread.polling(),))


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        # format='[%(asctime)s] {%(pathname)s:%(lineno)d} %(levelname)s - %(message)s',
        datefmt='%H:%M:%S'
    )

    thread_run()

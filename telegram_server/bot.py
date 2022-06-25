from typing import Callable

import dotenv
from telegram.ext import Application, MessageHandler, filters

from .utils import call_decorator


class BotThread:
    isAlive: bool = True
    _callbacks: list[Callable] = list()

    def __init__(self) -> None:
        self._token = dotenv.dotenv_values('telegram_server/.env')['TG_TOKEN']
        self.application = None

    def add_callback(self, callback: Callable):
        self._callbacks.append(callback)

    # @call_decorator
    async def send_message(self, chat_id: int, message_text: str):
        await self.application.bot.send_message(
            chat_id=chat_id,
            text=message_text,
        )

    def polling(self):
        self.application = Application.builder().token(self._token).build()

        builder = self.application.builder()
        builder.pool_timeout(100000000)

        handler = self._callbacks[0]

        text_handler = MessageHandler(filters.TEXT, handler)
        self.application.add_handler(text_handler)

        self.application.run_polling()

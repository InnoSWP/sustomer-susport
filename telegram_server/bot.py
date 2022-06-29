import time

import dotenv
from telegram.ext import MessageHandler, filters, Updater


class BotThread:
    # is_alive: bool = True
    # _callbacks: list[Callable] = list()

    def __init__(self, conn) -> None:
        self.conn = conn
        self._token = dotenv.dotenv_values('telegram_server/.env')['TG_TOKEN']
        self.application = None

    # def add_callback(self, callback: Callable):
    #     self._callbacks.append(callback)

    # @call_decorator
    async def send_message(self, chat_id: int, message_text: str):
        await self.application.bot.send_message(
            chat_id=chat_id,
            text=message_text,
        )

    @staticmethod
    def text_handler(update, context):
        print(update)

    def polling(self):
        updater = Updater(token=self._token, use_context=True)


        # self.application = Application.builder().token(self._token).build()

        # builder = self.application.builder()
        # builder.pool_timeout(100000000)

        # handler = self._callbacks[0]

        text_handler = MessageHandler(filters.Filters.text, self.text_handler)
        updater.dispatcher.add_handler(text_handler)

        updater.start_polling()
        updater.idle()

    def thread2(self):
        print('t2')
        while True:
            res = self.conn.recv()
            print('Res: ', res)
            time.sleep(1)

    def run(self):
        print(1)

        self.polling()
        # loop = asyncio.get_event_loop()
        # await self.polling()

        # self.thread2()

        # loop.create_task(self.polling())
        # loop.run_forever()
        # threading.Thread(target=loop.run_forever).start()

        # self.thread2()
        # p1 = threading.Thread(target=asyncio.run, args=(self.polling(),))
        # p2 = threading.Thread(target=self.thread2)

        # p1.start(); p2.start()
        # p1.join(); p2.join()
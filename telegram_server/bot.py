import logging
import threading
import dataclasses

import dotenv
import telegram
from telegram.ext import MessageHandler, Updater, filters

@dataclasses.dataclass
class DialogEntity:
    client_id: int
    volunteer_chat_id: int

    question_text: str
    answer_text: str

    state: int = None  # TODO make it enum

def search_by(entities_list, field, value):
    l = list(filter(
        lambda d: d.__getattribute__(field) == value,
        entities_list
    ))

    if len(l) == 1:
        return l[0]
    else:
        return None

class BotThread:
    dialogs: [DialogEntity]
    volunteers_id_list = []

    def __init__(self, conn) -> None:
        self.conn = conn
        self._token = dotenv.dotenv_values('telegram_server/.env')['TG_TOKEN']
        self.updater: Updater = Updater(token=self._token, use_context=True)

    def send_text_message(self, chat_id: int, message: str):
        return self.updater.bot.send_message(chat_id, message)

    def text_handler(self, update: telegram.Update, context):
        # TODO implement to handle if it in group or in personal messages

        chat_id = update.effective_chat.id
        client_id = search_by(self.dialogs, 'volunteer_chat_id', chat_id)

        if client_id:
            message_text = update.message.text

            self.conn.send([
                client_id,
                message_text
            ])

    def polling(self):
        print('TG T1 (polling)')

        text_message_handler = MessageHandler(filters.Filters.text, self.text_handler)
        self.updater.dispatcher.add_handler(text_message_handler)

        self.updater.start_polling()
        # updater.idle()

    def thread2(self):
        print('TG T2')
        while True:
            res = self.conn.recv()
            self.received_message_from_frontend(*res)

    def received_message_from_frontend(self, client_id: int, message: str):
        logging.info(f'TG: Received message from [FRONT-END - {client_id}] : {message}')

        # TODO New client
        # TODO Send message to group


    def run(self):
        fs = self.polling, self.thread2
        ps = [threading.Thread(target=f) for f in fs]

        [p.start() for p in ps]
        [p.join() for p in ps]

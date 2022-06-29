import logging
import threading
import json
from enum import Enum, IntEnum
from pydantic import BaseModel

import dotenv
import telegram
from telegram.ext import MessageHandler, Updater, filters
from telegram import InlineKeyboardButton, InlineKeyboardMarkup


class IssueState(IntEnum):
    open = 1
    progress = 2
    closed = 3


class ButtonData(BaseModel):
    state: IssueState
    # state:int
    issue_id: int


class BotThread:
    volunteers_id_list = []

    def __init__(self, conn) -> None:
        self.conn = conn
        self._token = dotenv.dotenv_values('telegram_server/.env')['TG_TOKEN']
        self.application = None

    def text_handler(self, update: telegram.Update, context):
        # TODO implement to handle if it in group or in personal messages

        chat_id = update.effective_chat.id
        message_text = update.message.text

        self.conn.send([
            chat_id,
            message_text
        ])
        data = ButtonData(state=IssueState.open, issue_id=1)
        update.message.reply_text(
            "test text", reply_markup=self.get_issue_buttons(data))

    def get_issue_buttons(self, button_data: ButtonData) -> InlineKeyboardMarkup:
        keyboard = [[InlineKeyboardButton(
            "hhahah", callback_data=button_data.json())]]
        return InlineKeyboardMarkup(keyboard)

    def polling(self):
        print('TG T1 (polling)')
        updater = Updater(token=self._token, use_context=True)

        text_message_handler = MessageHandler(
            filters.Filters.text, self.text_handler)
        updater.dispatcher.add_handler(text_message_handler)

        updater.start_polling()
        # updater.idle()

    def thread2(self):
        print('TG T2')
        while True:
            res = self.conn.recv()
            print('TG Recv: ', res)
            self.received_message_from_frontend(*res)

    def received_message_from_frontend(self, client_id, message: str):
        # TODO Main func invoked on receiving message from front-end
        logging.info(
            f'TG: Received message from [FRONT-END - {client_id}] : {message}')
        pass

    def run(self):
        print('TG process')

        fs = self.polling, self.thread2
        ps = [threading.Thread(target=f) for f in fs]

        [p.start() for p in ps]
        [p.join() for p in ps]

import logging
import threading
from enum import IntEnum
from pydantic import BaseModel

import dotenv
import telegram
from dataclasses import dataclass
from typing import TypeVar, Union
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


@dataclass
class DialogEntity:
    client_id: int
    volunteer_chat_id: int

    question_text: str = ''
    answer_text: str = ''

    state: IssueState = IssueState.open


T = TypeVar('T')


def search_by(entities_list: [T], field, value) -> Union[T, None]:
    l = list(filter(
        lambda d: d.__getattribute__(field) == value,
        entities_list
    ))

    if len(l) == 1:
        return l[0]
    else:
        return None


class BotThread:
    dialogs: [DialogEntity] = []
    volunteers_id_list = []

    def __init__(self, conn) -> None:
        self.conn = conn
        self._token = dotenv.dotenv_values('telegram_server/.env')['TG_TOKEN']
        self.updater: Updater = Updater(token=self._token, use_context=True)

    def send_text_message(self, chat_id: int, message: str):
        return self.updater.bot.send_message(
            chat_id,
            message
        )

    def text_handler(self, update: telegram.Update, context):
        group_chat_id = 12345  # TODO move to config

        chat_id = update.effective_chat.id

        if group_chat_id == chat_id:
            return  # Message from group/channel

        dialog: DialogEntity = search_by(self.dialogs, 'volunteer_chat_id', chat_id)

        if dialog:
            message_text = update.message.text
            dialog.answer_text += '\n' + message_text

            self.conn.send([
                dialog.client_id,
                message_text
            ])

        # TODO Just for test
        data = ButtonData(state=IssueState.open, issue_id=1)
        update.message.reply_text(
            "test text", reply_markup=self.get_issue_buttons(data))

    def get_issue_buttons(self, button_data: ButtonData) -> InlineKeyboardMarkup:
        keyboard = [[InlineKeyboardButton(
            "hhahah", callback_data=button_data.json())]]
        return InlineKeyboardMarkup(keyboard)

    def polling(self):
        print('TG T1 (polling)')

        text_message_handler = MessageHandler(
            filters.Filters.text, self.text_handler)
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

        if True:  # TODO If chained tg user & client
            accepted_chat_id = 325805942  # TODO [TEST] User that accepted to answer

            self.send_text_message(accepted_chat_id, f'You are assigned to the question:\n\n{message}')

            d = DialogEntity(
                client_id=client_id,
                volunteer_chat_id=accepted_chat_id
            )

            self.dialogs.append(d)

    def run(self):
        fs = self.polling, self.thread2
        ps = [threading.Thread(target=f) for f in fs]

        [p.start() for p in ps]
        [p.join() for p in ps]

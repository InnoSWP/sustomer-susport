import json
import logging
import pprint
import threading
from dataclasses import dataclass
from enum import IntEnum
from typing import TypeVar, Union

import dotenv
import telegram
from telegram.ext import MessageHandler, Updater, filters, CallbackQueryHandler

from .utils import get_button_markup


class IssueState(IntEnum):
    open = 1
    progress = 2
    closed = 3

@dataclass
class DialogEntity:
    issue_id: int

    client_id: int
    volunteer_chat_id: Union[int, None] = None

    question_text: str = ''
    answer_text: str = ''

    state: IssueState = IssueState.open


T = TypeVar('T')


def search_by(entities_list: [T], field, value) -> Union[T, None]:
    l = list(filter(
        lambda d: d.__getattribute__(field) == value,
        entities_list
    ))

    if len(l) >= 1:  # TODO manage it
        return l[0]
    else:
        return None


class BotThread:
    dialogs: [DialogEntity] = []
    issues_count: int = 0
    volunteers_id_list = []

    def __init__(self, conn) -> None:
        self.conn = conn
        self._token = dotenv.dotenv_values('telegram_server/.env')['TG_TOKEN']
        self.updater: Updater = Updater(token=self._token, use_context=True)

    def send_text_message(
            self,
            chat_id: int,
            message: str,
            reply_markup: telegram.ReplyMarkup = None
    ):
        return self.updater.bot.send_message(
            chat_id=chat_id,
            text=message,
            reply_markup=reply_markup
        )

    def text_handler(self, update: telegram.Update, _):
        # group_chat_id = 12345  # TODO move to config

        chat_id = update.effective_chat.id
        print(chat_id)

        # if group_chat_id == chat_id:
        #     return  # Message from group/channel

        dialog: DialogEntity = search_by(self.dialogs, 'volunteer_chat_id', chat_id)

        if dialog:
            message_text = update.message.text
            dialog.answer_text += '\n' + message_text

            self.conn.send([
                dialog.client_id,
                message_text
            ])

    def callback_query_handler(self, update: telegram.Update, context: telegram.ext.CallbackContext):
        data_dict = json.loads(update.callback_query.data)
        pprint.pprint(update.to_dict())

        issue_id: int = data_dict.get('issue_id', None)

        d: Union[DialogEntity, None] = search_by(self.dialogs, 'issue_id', issue_id)

        accepted_chat_id = update.callback_query.from_user.id
        self.send_text_message(accepted_chat_id, f'You are assigned to the [client {d.client_id}]\n'
                                                 f'with question:\n\n{d.question_text}')

        d.volunteer_chat_id = accepted_chat_id
        d.state = IssueState.progress

    def polling(self):
        print('TG T1 (polling)')

        handlers = [
            MessageHandler(filters.Filters.text, self.text_handler),
            CallbackQueryHandler(self.callback_query_handler),
        ]

        [self.updater.dispatcher.add_handler(i) for i in handlers]

        self.updater.start_polling()
        # updater.idle()

    def thread2(self):
        print('TG T2')
        while True:
            res = self.conn.recv()
            self.received_message_from_frontend(*res)

    def received_message_from_frontend(self, client_id: int, message: str):
        logging.info(f'TG: Received message from [FRONT-END - {client_id}] : {message}')

        group_chat_id = -1001412474288  # TODO move to config or whatever

        self.issues_count += 1
        new_issue_id = self.issues_count

        d = DialogEntity(
            issue_id=new_issue_id,
            client_id=client_id,
            volunteer_chat_id=None,
            question_text=message
        )
        self.dialogs.append(d)

        btn_data = json.dumps({'issue_id': new_issue_id})
        keyboard = get_button_markup(['Take it', btn_data])

        self.send_text_message(
            group_chat_id,
            f'bla bla take it take it\n\n{message}',
            reply_markup=keyboard,
        )

    def run(self):
        fs = self.polling, self.thread2
        ps = [threading.Thread(target=f) for f in fs]

        [p.start() for p in ps]
        [p.join() for p in ps]

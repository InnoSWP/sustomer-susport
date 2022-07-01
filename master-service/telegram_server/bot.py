import enum
import functools
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


class IssueState(enum.Enum):
    open = 'OPEN'
    progress = 'IN PROGRESS'
    closed = 'CLOSED'

    def __str__(self):
        return self.value.__str__()


class CallbackQueryType(IntEnum):
    ASSIGN = 1
    CLOSE = 2
    REJECT = 3

    def __str__(self):
        return self.value.__str__()


@dataclass
class DialogEntity:
    issue_id: int
    client_id: int

    volunteer_chat_id: Union[int, None] = None

    question_text: str = ''
    answer_text: str = ''

    issue_message_id: Union[int, None] = None
    state: IssueState = IssueState.open


def get_issue_message_text(dialog: DialogEntity, user_name=None):
    if dialog.state == IssueState.open:
        return f'*Issue #{dialog.issue_id}*\n\n' \
               f'{dialog.question_text}\n\n' \
               f'status: *OPEN*'
    elif dialog.state == IssueState.closed:
        return f'*Issue #{dialog.issue_id}*\n\n' \
               f'{dialog.question_text}\n\n' \
               f'Answers:\n{dialog.answer_text}'
    elif dialog.volunteer_chat_id and dialog.state == IssueState.progress:
        return f'*Issue #{dialog.issue_id}*\n\n' \
               f'{dialog.question_text}\n\n' \
               f'status: *IN PROGRESS* by {user_name}'
    else:
        return f'LOL why does this happen?'


T = TypeVar('T')
def search_by(entities_list: [T], field, value) -> Union[T, None]:
    l = list(filter(
        lambda d: d.__getattribute__(field) == value,
        entities_list
    ))

    if len(l) >= 1:  # TODO manage it
        return l[-1]
    else:
        return None


def keyboard_from_dialog(title: str, dialog: DialogEntity, btn_type: CallbackQueryType, group_message_id):
    btn_data = json.dumps({
        'issue_id': dialog.issue_id,
        'btn_type': btn_type,
        'group_message_id': group_message_id
    })
    return get_button_markup([title, btn_data])

def prepare_for_markdown_mode(message: str):
    message = message.replace('#', '\#')
    message = message.replace('-', '\-')
    message = message.replace('.', '\.')

    return message

class BotThread:
    dialogs: [DialogEntity] = []
    issues_count: int = 0
    volunteers_id_list = []
    group_chat_id = -1001412474288  # TODO move to config or whatever

    def __init__(self, conn) -> None:
        self.conn = conn
        self._token = dotenv.dotenv_values('telegram_server/.env')['TG_TOKEN']
        self.updater: Updater = Updater(token=self._token, use_context=True)

    def existing_dialogs(self, for_chat_id):
        return list(filter(
            lambda d: d.volunteer_chat_id == for_chat_id and d.state == IssueState.progress,
            self.dialogs
        ))

    def send_text_message(
            self,
            chat_id: int,
            message: str,
            reply_markup: telegram.ReplyMarkup = None,
            is_markdown=False
    ):
        try:
            return self.updater.bot.send_message(
                chat_id=chat_id,
                text=prepare_for_markdown_mode(message) if is_markdown else message,
                reply_markup=reply_markup,
                parse_mode=telegram.ParseMode.MARKDOWN_V2 if is_markdown else None
            )
        except Exception:
            return self.updater.bot.send_message(
                chat_id=chat_id,
                text=message,
                reply_markup=reply_markup,
            )

    def received_message_from_frontend(self, client_id: int, message: str):
        logging.info(f'TG: Received message from [FRONT-END - {client_id}] : {message}')

        self.issues_count += 1
        new_issue_id = self.issues_count

        d = DialogEntity(
            issue_id=new_issue_id,
            client_id=client_id,
            volunteer_chat_id=None,
            question_text=message
        )
        self.dialogs.append(d)

        message: telegram.Message = self.send_text_message(
            self.group_chat_id,
            message=get_issue_message_text(d),
            reply_markup=keyboard_from_dialog('Take request', d, CallbackQueryType.ASSIGN, None),
            is_markdown=True
        )

        d.issue_message_id = message.message_id

    def text_handler(self, update: telegram.Update, _):
        chat_id = update.effective_chat.id
        print(chat_id)

        print(self.dialogs)

        dialogs = self.existing_dialogs(chat_id)

        if len(dialogs) > 0:
            dialog = dialogs[-1]

            message_text = update.message.text
            dialog.answer_text += f'- {message_text}\n'

            self.conn.send([
                dialog.client_id,
                message_text
            ])
        else:
            # self.send_text_message(chat_id, 'You have no active issues')
            pass

    def callback_query_handler(self, update: telegram.Update, context: telegram.ext.CallbackContext):
        data_dict = json.loads(update.callback_query.data)
        # pprint.pprint(update.to_dict())

        issue_id: int = data_dict.get('issue_id', None)
        btn_type = data_dict.get('btn_type', None)

        print(self.dialogs, issue_id, btn_type)

        d: Union[DialogEntity, None] = search_by(self.dialogs, 'issue_id', issue_id)
        user_chat_id = update.callback_query.from_user.id
        message_id = update.effective_message.message_id
        user_name = update.callback_query.from_user.name

        existing_user_dialogs = self.existing_dialogs(user_chat_id)

        get_edit_text = lambda d: prepare_for_markdown_mode(
            get_issue_message_text(d, user_name)
        )

        if int(btn_type) == CallbackQueryType.ASSIGN:
            group_chat_id = update.effective_chat.id

            if len(existing_user_dialogs) > 0:
                return self.send_text_message(group_chat_id, f'{user_name}, you already have active issue')

            d.volunteer_chat_id = user_chat_id
            d.state = IssueState.progress

            message_text = f'You are assigned to the [client {d.client_id}]\n' \
                           f'with question:\n\n{d.question_text}'

            update.effective_message.edit_text(
                text=get_edit_text(d),
                parse_mode=telegram.ParseMode.MARKDOWN_V2
            )

            self.send_text_message(
                user_chat_id,
                message_text,
                reply_markup=keyboard_from_dialog('Mark as completed', d, CallbackQueryType.CLOSE, message_id)
            )
        elif int(btn_type) == CallbackQueryType.CLOSE:
            if d.state == IssueState.closed:
                return

            d.state = IssueState.closed

            self.send_text_message(
                chat_id=user_chat_id,
                message=get_issue_message_text(d, user_name),
                is_markdown=True
            )

            context.bot.edit_message_text(
                text=get_edit_text(d),
                chat_id=self.group_chat_id,
                message_id=d.issue_message_id,
                parse_mode=telegram.ParseMode.MARKDOWN_V2
            )

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

    def run(self):
        fs = self.polling, self.thread2
        ps = [threading.Thread(target=f) for f in fs]

        [p.start() for p in ps]
        [p.join() for p in ps]

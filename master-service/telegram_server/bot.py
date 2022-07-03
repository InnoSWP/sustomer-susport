import os
import json
import logging
import threading
from typing import Optional, Union

import requests
import telegram
from telegram.ext import MessageHandler, CommandHandler
from telegram.ext import MessageHandler, Updater, filters, CallbackQueryHandler


from .utils import DialogEntity, IssueState, prepare_for_markdown_mode, \
    search_by, get_issue_message_text, keyboard_from_dialog, CallbackQueryType

TG_TOKEN = os.getenv('TG_TOKEN', None)
GROUP_CHAT_ID = os.getenv('GROUP_CHAT_ID', None)

USE_NLP_ROUTER = os.getenv('USE_NLP_ROUTER', 'True').lower() == 'true'
NLP_ROUTER_URL = os.getenv('NLP_ROUTER_URL', 'http://127.0.0.1:8080')

class BotThread:
    dialogs: [DialogEntity] = []
    issues_count: int = 0
    volunteers_id_list = []

    def __init__(self, conn) -> None:
        self.conn = conn
        self.updater: Updater = Updater(token=TG_TOKEN, use_context=True)

    def existing_dialogs(self, for_chat_id):
        return list(filter(
            lambda d: d.volunteer_chat_id == for_chat_id and d.state == IssueState.progress,
            self.dialogs
        ))

    def send_text_message(
            self,
            chat_id: Union[int, str],
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
            GROUP_CHAT_ID,
            message=get_issue_message_text(d),
            reply_markup=keyboard_from_dialog('Take request', d, CallbackQueryType.ASSIGN, None),
            is_markdown=True
        )

        d.issue_message_id = message.message_id

    def text_handler(self, update: telegram.Update, _):
        chat_id = update.effective_chat.id
        print(chat_id)

        # print(self.dialogs)

        dialogs: list[DialogEntity] = self.existing_dialogs(chat_id)

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

        d: Optional[DialogEntity] = search_by(self.dialogs, 'issue_id', issue_id)

        if not d:
            return

        user_chat_id = update.callback_query.from_user.id
        message_id = update.effective_message.message_id
        user_name = update.callback_query.from_user.name.replace("_", "\\_")

        existing_user_dialogs = self.existing_dialogs(user_chat_id)

        get_edit_text = lambda d: prepare_for_markdown_mode(
            get_issue_message_text(d, user_name)
        )

        if int(btn_type) == CallbackQueryType.ASSIGN:
            group_chat_id = update.effective_chat.id

            if len(existing_user_dialogs) > 0:
                return self.send_text_message(group_chat_id, f'{user_name}, you already have active issue')

            if d.state != IssueState.open:
                return

            d.volunteer_chat_id = user_chat_id
            d.state = IssueState.progress

            message_text = f'You are assigned to the [client {d.client_id}]\n' \
                           f'with question:\n\n{d.question_text}'

            try:
                update.effective_message.edit_text(
                    text=get_edit_text(d),
                    parse_mode=telegram.ParseMode.MARKDOWN_V2
                )
            except Exception:
                update.effective_message.edit_text(
                    text=get_edit_text(d)
                )

            self.send_text_message(
                user_chat_id,
                message_text,
                reply_markup=keyboard_from_dialog('Mark as completed', d, CallbackQueryType.CLOSE, message_id)
            )
        elif int(btn_type) == CallbackQueryType.CLOSE:
            self.on_issue_close(d, user_chat_id, user_name, context.bot)

    def on_issue_close(self,
                       d: DialogEntity,
                       user_chat_id: Union[str, int],
                       user_name: str,
                       bot: telegram.Bot,):
        get_edit_text = lambda d: prepare_for_markdown_mode(
            get_issue_message_text(d, user_name)
        )

        if d.state != IssueState.progress:
            return

        d.state = IssueState.closed

        self.send_text_message(
            chat_id=user_chat_id,
            message=get_issue_message_text(d, user_name),
            is_markdown=True
        )

        if USE_NLP_ROUTER:
            try:
                url = f'{NLP_ROUTER_URL}/new-question'
                resp = requests.post(url, json={
                    'question': d.question_text,
                    'answer': d.answer_text,
                })

                logging.info(f'Made request to NLP: {resp.url}')
            except Exception:
                pass

        try:
            bot.edit_message_text(
                text=get_edit_text(d),
                chat_id=GROUP_CHAT_ID,
                message_id=d.issue_message_id,
                parse_mode=telegram.ParseMode.MARKDOWN_V2
            )
        except Exception:
            bot.edit_message_text(
                text=get_edit_text(d),
                chat_id=GROUP_CHAT_ID,
                message_id=d.issue_message_id
            )

    def on_submit_button(self, update: telegram.Update, context: telegram.ext.CallbackContext):
        chat_id = update.effective_chat.id
        user_name = update.effective_user.name.replace("_", "\\_")

        existing_dialogs = self.existing_dialogs(chat_id)
        cur_dialog = existing_dialogs[-1]

        self.on_issue_close(
            cur_dialog,
            chat_id,
            user_name,
            context.bot
        )

    def polling(self):
        print('TG T1 (polling)')

        handlers = [
            CommandHandler('submit', self.on_submit_button),
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

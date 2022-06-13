import os

from typing import Callable

from flask import Flask, request, render_template
from telegram import Update
from telegram.ext import CallbackContext

from utils import call_decorator


class FlaskThread:
    _callbacks: list[Callable] = list()

    def __init__(self):
        self.app = Flask(__name__)
        self.app.config['SECRET_KEY'] = os.urandom(12)

        self.app.add_url_rule('/', view_func=self.index)
        self.app.add_url_rule('/frame', view_func=self.frame_get, methods=['GET'])
        self.app.add_url_rule('/messages', view_func=self.messages_post, methods=['POST'])

    def add_callback(self, callback: Callable):
        self._callbacks.append(callback)

    # Invoked by handler trigger
    @call_decorator
    async def send_some_api_to_front_callback(self, update: Update, _: CallbackContext.DEFAULT_TYPE):
        chat_id = update.effective_chat.id

        send_message = self._callbacks[0]

        await send_message(chat_id, update.message.text + '123')

    def run(self):
        return self.app.run()

    @staticmethod
    def index():
        """
        /, [GET]
        """
        return render_template("index.html")

    @staticmethod
    def frame_get():
        """
        /frame, [GET]
        """
        return render_template('form.html')

    def messages_post(self):
        """
        /messages [POST]
        JSON Format:
            {
                user_id: int
                text: str
            }
        """

        data: dict = request.json

        text = data.get('text', None)
        user_id = data.get('user_id', None)

        message_to_send = f'{user_id}: {text}'

        send_message = self._callbacks[0]
        send_message(0, message_to_send)

        return 'niceee'

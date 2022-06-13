from typing import Callable

from flask import Flask, request, render_template
from telegram import Update
from telegram.ext import CallbackContext

from utils import call_decorator


class FlaskThread:
    _callbacks: list[Callable] = list()

    def __init__(self):
        self.app = Flask(__name__)
        self.app.config['SECRET_KEY'] = 'huy'

        self.app.add_url_rule('/', view_func=self.index)
        self.app.add_url_rule('/frame', view_func=self.frame_get, methods=['GET'])
        self.app.add_url_rule('/messages', view_func=self.messages_post, methods=['POST'])

    def add_callback(self, callback: Callable):
        self._callbacks.append(callback)

    @call_decorator
    async def send_some_api_to_front_callback(self, update: Update, context: CallbackContext.DEFAULT_TYPE):
        chat_id = update.effective_chat.id
        bot = context.bot

        send_message = self._callbacks[0]

        await send_message(bot, chat_id, update.message.text + '123')

    def run(self):
        return self.app.run()

    # @app.route("/", methods=['GET'])
    def index(self):
        return render_template("index.html")

    # @app.route("/frame", methods=['GET'])
    def frame_get(self):
        # token = data.args.get('token')

        # if not token:
        #     return redirect('/')

        # response = requests.get('bot-api', params={'token': token})
        # frame = response.json()['frame']

        # return frame

        return render_template('form.html')

    # @app.route("/messages", methods=['POST'])
    def messages_post(self):
        data: dict = request.json
        text = data.get('text', None)
        user_id = data.get('user_id', None)
        return "nice"

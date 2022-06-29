import os
import dotenv
import requests
from flask import Flask, jsonify, render_template, request
from flask_wtf.csrf import CSRFProtect


class FlaskThread:
    NLP_CHECK = False
    messages_to_proceed: list[str] = []

    def __init__(self, conn):
        self.conn = conn
        self.app = Flask(__name__)
        # csrf = CSRFProtect()
        # csrf.init_app(self.app)
        self.app.config['SECRET_KEY'] = os.urandom(12)

        self.app.add_url_rule('/', view_func=self.index)
        self.app.add_url_rule(
            '/frame', view_func=self.frame_get, methods=['GET'])
        self.app.add_url_rule(
            '/messages', view_func=self.messages_post, methods=['POST'])
        self.app.add_url_rule(
            '/messages', view_func=self.messages_get, methods=['GET'])

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

    def messages_get(self):
        """
        /messages [GET]
        """

        result = jsonify(self.messages_to_proceed)
        self.messages_to_proceed = []

        return result

    async def send_to_tg(self, user_id, text):
        message_to_send = f'{user_id}: {text}'

        # send_message = self._callbacks[0]

        chat_id = dotenv.dotenv_values('flask_server/.env')['TEST_CHAT_ID']
        # await send_message(chat_id, message_to_send)
        self.conn.send([chat_id, message_to_send])

    async def messages_post(self):
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

        if self.NLP_CHECK:
            base_nlp_router_url = 'http://127.0.0.1:8000'
            similar_endpoint = '/similar'
            result_url = f'{base_nlp_router_url}{similar_endpoint}'

            resp = requests.get(result_url, {'question': text})
            print(">>>" * 5)
            print(resp.url)
            print("<<<" * 5)

            if len(resp.json()) != 0:
                return jsonify(resp.json())

        await self.send_to_tg(user_id, text)

        return 'niceee'

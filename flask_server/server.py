import logging
import os
import threading

import requests
from flask import Flask, jsonify, render_template, request


class FlaskThread:
    NLP_CHECK = True
    answers_to_proceed: {int: str}  # client_id: text

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

    def thread2(self):
        print('Flask T2')
        while True:
            res = self.conn.recv()
            self.received_text_message_from_tg(*res)

    def received_text_message_from_tg(self, client_id: int, message_text: str):
        logging.info(f'Received text message to [Client - {client_id}] : {message_text}')

        self.answers_to_proceed[client_id] = message_text

    def send_to_telegram(self, client_id: int, message_text: str):
        self.conn.send([
            client_id,
            message_text
        ])

    def flask_run(self):
        print('Flask T1 (app.run)')
        return self.app.run()

    def run(self):
        fs = self.flask_run, self.thread2
        ps = [threading.Thread(target=f) for f in fs]

        [p.start() for p in ps]
        [p.join() for p in ps]

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

        # TODO Return id cookies
        return render_template('form.html')

    def messages_get(self):
        """
        Invoked on poll request from Front-end to get all messages (including updated)

        /messages [GET]
        """

        client_id: int = 0  # TODO get from cookies

        answer = self.answers_to_proceed.get(client_id, None)

        if answer:
            self.answers_to_proceed[client_id] = None

            return jsonify(answer)
        else:
            return jsonify(None)

    async def messages_post(self):
        """
        Invoked on new message from Front-end part

        /messages [POST]
        JSON Format:
            {
                user_id: int
                text: str
            }
        """

        data: dict = request.json

        client_id: int = 0  # TODO get from cookies
        message_text = data.get('text', None)

        if self.NLP_CHECK:
            base_nlp_router_url = 'http://127.0.0.1:8000'
            similar_endpoint = '/similar'
            result_url = f'{base_nlp_router_url}{similar_endpoint}'

            resp = requests.get(result_url, {'question': message_text})

            if len(resp.json()) != 0:
                return jsonify(resp.json())

        # Send to Telegram in case of no answer from NLP_router
        self.send_to_telegram(client_id, message_text)

        return 'niceee'

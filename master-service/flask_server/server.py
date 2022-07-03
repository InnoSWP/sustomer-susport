import logging
import os
import threading

import requests
from flask import Flask, jsonify, render_template, request, make_response

USE_NLP_ROUTER = os.getenv('USE_NLP_ROUTER', 'True').lower() == 'true'
NLP_ROUTER_URL = os.getenv('NLP_ROUTER_URL', 'http://127.0.0.1:8080')

class FlaskThread:
    answers_to_proceed: {int: list[str]} = dict()

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

        if client_id in self.answers_to_proceed:
            self.answers_to_proceed[client_id].append(message_text)
        else:
            self.answers_to_proceed[client_id] = [message_text, ]
        print(self.answers_to_proceed)

    def send_to_telegram(self, client_id: int, message_text: str):
        self.conn.send([
            client_id,
            message_text
        ])

    def flask_run(self):
        print('Flask T1 (app.run)')
        return self.app.run(
            host="0.0.0.0",
            port=5000
        )

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

        import random
        client_id = random.randint(10 ** 5, 10 ** 6)

        response = make_response(render_template('form.html'))
        response.set_cookie('userID', str(client_id))

        return response

    def messages_get(self):
        """
        Invoked on poll request from Front-end to get all messages (including updated)

        /messages [GET]
        """

        client_id: int = int(request.cookies.get('userID'))

        answer = self.answers_to_proceed.get(client_id, None)
        print('answer', answer)

        if answer:
            self.answers_to_proceed[client_id] = None

            return jsonify(answer)
        else:
            # I would to kill guy that returned None!
            return jsonify([])

    def messages_post(self):
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

        client_id: int = int(request.cookies.get('userID'))
        message_text = data.get('text', None)

        if USE_NLP_ROUTER:
            result_url = f'{NLP_ROUTER_URL}/similar'

            resp = requests.get(result_url, {'question': message_text})

            most_similar: dict = resp.json()

            if len(most_similar) > 0:
                return jsonify(most_similar)

        # Send to Telegram in case of no answer from NLP_router
        self.send_to_telegram(client_id, message_text)

        return "OK"

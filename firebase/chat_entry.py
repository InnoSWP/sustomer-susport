from datetime import datetime


class ChatMessage:
    message: str
    time: datetime
    user_sent: bool

    def __init__(self, message, user_sent=False, time=None):
        self.message = message
        self.user_sent = user_sent
        if not time:
            time = datetime.now()
        self.time = time

    def to_dict(self):
        return {"message": self.message, "user_sent": self.user_sent, "time": self.time}


class ChatEntry:
    _chat_id: str
    is_open: bool
    messages: list[ChatMessage]
    '''
    Message format:
    {
        "message": [str],
        "is_open": [bool],
        "time": [datetime]
    }
    '''

    def __init__(self, chat_id, messages=None, is_open=True):
        if messages is None:
            messages = []

        self._chat_id = chat_id
        self.is_open = is_open
        self.messages = messages

    def __str__(self):
        return self._chat_id

    def __eq__(self, other):
        return self.chat_id == other.chat_id

    def to_dict(self):
        return {"chat_id": self._chat_id, "is_open": self.is_open, "messages": [m.to_dict() for m in self.messages]}

    @property
    def chat_id(self):
        return self._chat_id

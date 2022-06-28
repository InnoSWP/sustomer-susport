class ChatEntry:
    _chat_id: str
    is_open: bool
    messages: list[dict]

    def __init__(self, chat_id, messages=None):
        if messages is None:
            messages = []

        self._chat_id = chat_id
        self.is_open = True
        self.messages = messages

    def __str__(self):
        return self._chat_id

    def __eq__(self, other):
        return self.chat_id == other.chat_id

    def to_dict(self):
        pass

    @property
    def chat_id(self):
        return self._chat_id

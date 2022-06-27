class ChatEntry:
    _chat_id: str
    messages: [str]

    def __init__(self):
        # TODO
        # raise NotImplemented
        pass

    def __str__(self):
        return self._chat_id + ' ' + ' '.join(self.messages)

    def __eq__(self, other):
        return self.chat_id == other.chat_id

    @property
    def chat_id(self):
        return self._chat_id

class QuestionEntry:
    # _question_key - temporarily made to be string
    _key: str
    answer: str

    def __init__(self, key: str, answer: str):
        self._key = key
        self.answer = answer

    def __str__(self):
        return self._key

    @property
    def key(self):
        return self._key

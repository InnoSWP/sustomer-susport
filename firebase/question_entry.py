class QuestionEntry:
    _key: str
    question: str
    answer: str

    def __init__(self, key: str, question: str, answer: str):
        self._key = key
        self.question = question
        self.answer = answer

    def __str__(self):
        return self.question

    def __eq__(self, other):
        return (self.key == other.key) and (self.question == other.question) and (self.answer == other.answer)

    @property
    def key(self):
        return self._key

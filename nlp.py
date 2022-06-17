from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from firebase.question_entry import QuestionEntry


class absSimProvider:
    @classmethod
    def encode_question(cls, question: str) -> str:
        return ''

    @staticmethod
    def similarity(q1: QuestionEntry, q2: QuestionEntry) -> float:
        return 0


class susSimProvider(absSimProvider):
    model = SentenceTransformer('bert-base-nli-mean-tokens')

    @classmethod
    def encode_question(cls, question: str) -> str:
        return str(cls.model.encode(question).tolist())

    @staticmethod
    def similarity(q1: QuestionEntry, q2: QuestionEntry) -> float:
        return cosine_similarity([eval(q1.key)], [eval(q2.key)])[0][0]


if __name__ == "__main__":
    model = susSimProvider

    print("The model is loaded")

    q1 = "What is the strongest muscle in the humans bpdy?"
    q2 = "Human's body best muscle"
    q3 = "Why is Linus Torvalds so genius?"

    qe1 = QuestionEntry(model.encode_question(q1), q1, 'jaw')
    qe2 = QuestionEntry(model.encode_question(q2), q2, '')
    qe3 = QuestionEntry(model.encode_question(q3), q3, '')

    print(model.similarity(qe1, qe2))
    print(model.similarity(qe1, qe3))
    print(model.similarity(qe2, qe3))

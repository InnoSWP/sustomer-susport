from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity


class absSimProvider:
    @classmethod
    def encode_question(cls, question: str) -> str:
        return ''

    @staticmethod
    def similarity(q1_key: str, q2_key: str) -> float:
        return 0


class susSimProvider(absSimProvider):
    model = SentenceTransformer('bert-base-nli-mean-tokens')

    @classmethod
    def encode_question(cls, question: str) -> str:
        return str(cls.model.encode(question).tolist())

    @staticmethod
    def similarity(q1_key: str, q2_key: str) -> float:
        return cosine_similarity([eval(q1_key)], [eval(q2_key)])[0][0]


if __name__ == "__main__":

    print("The model is loaded")

    q1 = "What is the strongest muscle in the humans bpdy?"
    q2 = "Human's body best muscle"
    q3 = "Why is Linus Torvalds so genius?"

    qe1 = susSimProvider.encode_question(q1)
    qe2 = susSimProvider.encode_question(q2)
    qe3 = susSimProvider.encode_question(q3)

    print(susSimProvider.similarity(qe1, qe2))
    print(susSimProvider.similarity(qe1, qe3))
    print(susSimProvider.similarity(qe2, qe3))

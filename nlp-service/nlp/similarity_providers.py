from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity


class abs_sim_provider:
    @classmethod
    def encode_question(cls, question: str) -> str:
        return ''

    @staticmethod
    def similarity(q1_key: str, q2_key: str) -> float:
        return 0


class sus_sim_provider(abs_sim_provider):
    model = SentenceTransformer('bert-base-nli-mean-tokens')

    @classmethod
    def encode_question(cls, question: str) -> str:
        return str(cls.model.encode(question).tolist())

    @staticmethod
    def similarity(q1_key: str, q2_key: str) -> float:
        return cosine_similarity([eval(q1_key)], [eval(q2_key)])[0][0]

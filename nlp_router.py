import uvicorn
from starlette.status import HTTP_201_CREATED, HTTP_404_NOT_FOUND
from firebase.firestore_database import FirestoreDatabase
from firebase.question_entry import QuestionEntry
from fastapi import FastAPI, Response
from pydantic import BaseModel

from nlp.similarity_providers import sus_sim_provider

SIMILARITY_CONST = 0.75
app = FastAPI()
cached_questions: list[QuestionEntry] = []
fd = FirestoreDatabase("firebase/sustomer-susport-private-key.json")


class QuestionItem(BaseModel):
    question: str
    answer: str


@app.on_event("startup")
def init():
    global cached_questions, fd
    cached_questions = fd.questions()


@app.get("/", status_code=404)
def index():
    return Response(status_code=HTTP_404_NOT_FOUND)


@app.get("/similar")
def similar_questions(question: str, index: float = SIMILARITY_CONST):
    """
    /similar [GET]
    :param question : question text
    :param index : similarity threshold
    """
    global cached_questions
    question_key = sus_sim_provider.encode_question(question)
    top_similar = []
    for q in cached_questions:
        try:
            cur_sim = sus_sim_provider.similarity(question_key, q.key)
            if cur_sim > index:
                top_similar.append({"question": q.question, "answer": q.answer, "index": cur_sim})
        except NameError:
            pass

    return top_similar


@app.post("/new", status_code=201)
def new_question(q_item: QuestionItem):
    global cached_questions, fd
    q_key = sus_sim_provider.encode_question(q_item.question)
    q_entry = QuestionEntry(q_key, q_item.question, q_item.answer)

    fd.set_question(q_entry)
    cached_questions = fd.questions()

    return Response(status_code=HTTP_201_CREATED)


def run_router():
    uvicorn.run(app, port=8000)


if __name__ == "__main__":
    run_router()

import uvicorn
from starlette.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_404_NOT_FOUND
from firebase.firestore_database import FirestoreDatabase
from firebase.question_entry import QuestionEntry
from fastapi import FastAPI, Response
from pydantic import BaseModel

from nlp.similarity_providers import sus_sim_provider

SIMILARITY_CONST = 0.7
app = FastAPI()
cached_questions: list[QuestionEntry] = []
fd = FirestoreDatabase()


class QuestionItem(BaseModel):
    question: str
    answer: str


@app.on_event("startup")
def init():
    global cached_questions

    cached_questions = fd.questions()


@app.get("/", status_code=404)
def index():
    return Response(status_code=HTTP_404_NOT_FOUND)


@app.get("/questions")
def get_questions():
    answer = [{"key": q.key, "question": q.question, "answer": q.answer} for q in cached_questions]
    return answer


@app.get("/question")
def get_question(question: str):
    answer = [{"key": q.key, "question": q.question, "answer": q.answer}
              for q in cached_questions if q.question == question]
    if answer:
        return answer[0]
    else:
        return Response(status_code=HTTP_404_NOT_FOUND)


@app.post("/new")
def set_question(q_item: QuestionItem):
    global cached_questions

    q_key = sus_sim_provider.encode_question(q_item.question)
    q_entry = QuestionEntry(q_key, q_item.question, q_item.answer)

    fd.set_question(q_entry)
    cached_questions = fd.questions()

    return Response(status_code=HTTP_201_CREATED)


@app.delete("/delete")
def delete_question(question: str):
    global cached_questions

    found = [q for q in cached_questions if q.question == question]
    if not found:
        return Response(status_code=HTTP_404_NOT_FOUND)

    fd.delete_question(question)
    cached_questions = fd.questions()

    return Response(status_code=HTTP_200_OK)


@app.get("/similar")
def similar_questions(question: str, index: float = SIMILARITY_CONST):
    """
    /similar [GET]
    :param question : question text
    :param index : similarity threshold
    """
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


def run_router():
    uvicorn.run(app, port=8080)


if __name__ == "__main__":
    run_router()

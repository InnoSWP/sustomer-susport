import os
import uvicorn
from fastapi import FastAPI, Response
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from firebase.firestore_database import FirestoreDatabase
from firebase.question_entry import QuestionEntry
from nlp.similarity_providers import sus_sim_provider

SIMILARITY_CONST = 0.7
app = FastAPI()
fd = FirestoreDatabase(app_name="nlp_router")

USE_NLP_ROUTER = os.getenv('USE_NLP_ROUTER', 'True').lower() == 'true'


class QuestionItem(BaseModel):
    question: str
    answer: str


@app.get("/", status_code=404)
def index():
    return Response(status_code=404)


@app.get("/questions")
def get_questions():
    cur_questions = fd.questions()

    answer = [q.to_dict() for q in cur_questions]
    return answer


@app.get("/question")
def get_question(question: str):
    cur_questions = fd.questions()

    answer = [q.to_dict() for q in cur_questions if q.question == question]
    if answer:
        return answer[0]
    else:
        return JSONResponse({"status": "Such question does not exist"}, status_code=404)


@app.post("/new-question")
def set_question(q_item: QuestionItem):
    q_key = sus_sim_provider.encode_question(q_item.question)
    q_entry = QuestionEntry(q_key, q_item.question, q_item.answer)

    fd.set_question(q_entry)

    return JSONResponse(q_entry.to_dict() | {"status": "created"}, status_code=201)


@app.delete("/delete-question")
def delete_question(question: str):
    cur_questions = fd.questions()

    found = [q for q in cur_questions if q.question == question]
    if not found:
        return JSONResponse({"status": "Such question does not exist"}, status_code=404)

    q = fd.get_question(question)
    fd.delete_question(question)

    return JSONResponse(q.to_dict() | {"status": "deleted"}, status_code=200)


@app.get("/similar")
def similar_questions(question: str, index: float = SIMILARITY_CONST):
    """
    /similar [GET]
    :param question : question text
    :param index : similarity threshold
    """
    cur_questions = fd.questions()

    question_key = sus_sim_provider.encode_question(question)
    top_similar = []
    for q in cur_questions:
        try:
            cur_sim = sus_sim_provider.similarity(question_key, q.key)
            if cur_sim > index:
                top_similar.append({"question": q.question, "answer": q.answer, "index": cur_sim})
        except NameError:
            pass

    return top_similar


def run_router():
    uvicorn.run(app=app, host="0.0.0.0", port=8080)


if __name__ == "__main__":
    if USE_NLP_ROUTER:
        run_router()
    else:
        print('USE_NLP_ROUTER = False')

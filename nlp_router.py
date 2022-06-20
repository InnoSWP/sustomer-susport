import uvicorn
from starlette.status import HTTP_201_CREATED, HTTP_404_NOT_FOUND
from firestore_database import FirestoreDatabase
from question_entry import QuestionEntry
from fastapi import FastAPI, Response
from pydantic import BaseModel

SIM_CONST = 0.75
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
def similar_questions(question: str, index: float = SIM_CONST):
    global cached_questions
    # TODO: search for similar question
    for q in cached_questions:
        print(f"{q.question}: {q.answer}")

    return {question: str(index)}


@app.post("/new", status_code=201)
def new_question(q_item: QuestionItem):
    global cached_questions, fd
    # TODO: get key by question
    q_key = "new_key"
    q_entry = QuestionEntry(q_key, q_item.question, q_item.answer)

    fd.set_question(q_entry)
    cached_questions = fd.questions()

    return Response(status_code=HTTP_201_CREATED)


def run_router():
    uvicorn.run(app, port=8000)


if __name__ == "__main__":
    run_router()

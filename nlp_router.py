import uvicorn
from firestore_database import FirestoreDatabase
from question_entry import QuestionEntry
from fastapi import FastAPI
from nlp import susSimProvider

SIM_CONST = 0.75
app = FastAPI()
cached_questions: list[QuestionEntry] = []
fd = FirestoreDatabase("firebase/sustomer-susport-private-key.json")


@app.on_event("startup")
def init():
    global cached_questions, fd
    cached_questions = fd.questions()


@app.get("/")
def root():
    global cached_questions
    for q in cached_questions:
        print(f"{q.question}: {q.answer}")
    return {"message": "Hello World"}


@app.get("/similar")
def similar_questions(question: str, index: float = SIM_CONST):
    global cached_questions
    for question in cached_questions:
        susSimProvider.encode_question(str)

    return {"question": question}


def run_router():
    uvicorn.run(app, port=8000)


if __name__ == "__main__":
    run_router()

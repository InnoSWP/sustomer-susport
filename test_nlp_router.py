from fastapi.testclient import TestClient

from nlp_router import app

client = TestClient(app)


def test_questions():
    response = client.get("/questions")
    assert response.status_code == 200

    questions = response.json()
    for q in questions:
        print(f"{q.question}: {q.answer}")


def test_question_funcs():
    initial_questions = client.get("/questions")

    question = {"question": "What is the hottest planet in our system?", "answer": "Venus"}

    # Add new question to firestore
    response = client.post("/new", json=question)
    assert response.status_code == 201

    assert client.get("/questions").json() != initial_questions.json()

    # Get that question
    response = client.get("/question", params={"question": "What is the hottest planet in our system?"})
    assert response.status_code == 200

    # Non-existing question
    response = client.get("/question", params={"question": "Non-existing question_WRWQFduhuw&333"})
    assert response.status_code == 404

    # Delete that question
    response = client.delete("/delete", params={"question": "What is the hottest planet in our system?"})
    assert response.status_code == 200

    # Non-existing question
    response = client.delete("/delete", params={"question": "Non-existing question_WRWQFduhuw&333"})
    assert response.status_code == 404

    assert client.get("/questions").json() == initial_questions.json()


def test_similar():

    question = {"question": "What is the strongest muscle in the human's bod?", "answer": "The teeth"}
    client.post("/new", json=question)

    response = client.get("/similar", params={"question": "Best people muscle which one?"})
    assert response.status_code == 200

    response = client.get("/similar", params={"question": "What is the best muscle in the people?", "index": "0.8"})
    assert response.status_code == 200

    response = client.delete("/delete", params={"question": "What is the strongest muscle in the human's bod?"})
    assert response.status_code == 200

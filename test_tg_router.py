from fastapi.testclient import TestClient

from tg_router import app

client = TestClient(app)


def test_teams():
    response = client.get("/teams")
    assert response.status_code == 200


def test_team_funcs():
    initial_teams = client.get("/teams")

    team = {"team_name": "sustem inc", "members": ['Boris', 'Timofei', 'Stepan', 'Nikita'], "tg_group_id": 123}

    # Add new team to firestore
    response = client.post("/new-team", json=team)
    assert response.status_code == 201

    assert client.get("/teams").json() != initial_teams.json()

    # Get that team
    response = client.get("/team", params={"team_name": "sustem inc"})
    assert response.status_code == 200

    # Non-existing team
    response = client.get("/team", params={"team_name": "Non-existing team&333"})
    assert response.status_code == 404

    # Delete that team
    response = client.delete("/delete-team", params={"team_name": "sustem inc"})
    assert response.status_code == 200

    # Non-existing team
    response = client.delete("/delete-team", params={"team_name": "Non-existing team&333"})
    assert response.status_code == 404

    assert client.get("/teams").json() == initial_teams.json()


def test_chats():
    response = client.get("/chats")
    assert response.status_code == 200


def test_chat_funcs():
    initial_chats = client.get("/chats")

    chat_1 = \
        {
            "chat_id": "test_chat_id_1_aaoiJWDooi325uoFJ",
            "is_open": True,
            "messages":
                [{
                    "message": "What does the fox say?",
                    "user_sent": True,
                    "time": "2022-06-27T15:44:54.694000+00:00"
                }]
        }
    chat_2 = \
        {
            "chat_id": "test_chat_id_2_aaoiJWDooi325uoFJ",
            "is_open": True
        }
    chat_3 = \
        {
            "chat_id": "test_chat_id_3_aaoiJWDooi325uoFJ",
            "is_open": True,
            "messages":
                [{
                    "message": "What does the fox say?"
                }]
        }

    # Add chats to firestore
    response = client.post("/new-chat", json=chat_1)
    assert response.status_code == 201

    response = client.post("/new-chat", json=chat_2)
    assert response.status_code == 201

    response = client.post("/new-chat", json=chat_3)
    assert response.status_code == 201
    # Try already existing chat
    response = client.post("/new-chat", json=chat_3)
    assert response.status_code == 409

    # Check that chats are updated
    assert client.get("/chats").json() != initial_chats.json()

    # Check that chats are properly loaded onto the firestore
    response = client.get("/chat", params={"chat_id": chat_1["chat_id"]})
    assert response.status_code == 200
    assert response.json() == chat_1

    response = client.get("/chat", params={"chat_id": chat_2["chat_id"]})
    assert response.status_code == 200
    assert response.json() == chat_2 | {"messages": []}

    response = client.get("/chat", params={"chat_id": chat_3["chat_id"]})
    assert response.status_code == 200
    # Try non-existing chat
    response = client.get("/chat", params={"chat_id": "non_existing_chat_id_aaoiJWDooi325uoFJ"})
    assert response.status_code == 404

    # Delete chats
    response = client.delete("/delete-chat", params={"chat_id": chat_1["chat_id"]})
    assert response.status_code == 200

    response = client.delete("/delete-chat", params={"chat_id": chat_2["chat_id"]})
    assert response.status_code == 200

    response = client.delete("/delete-chat", params={"chat_id": chat_3["chat_id"]})
    assert response.status_code == 200
    # Try non-existing chat
    response = client.delete("/delete-chat", params={"chat_id": "non_existing_chat_id_aaoiJWDooi325uoFJ"})
    assert response.status_code == 404

    # Check if you leave the things as they were initially
    assert client.get("/chats").json() == initial_chats.json()

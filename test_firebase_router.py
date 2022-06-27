from fastapi.testclient import TestClient

from firebase_router import app

client = TestClient(app)


def test_teams():
    response = client.get("/teams")
    assert response.status_code == 200

    teams = response.json()
    print()
    for team in teams:
        print(f"{team['team_name']}: {team['members']}, {team['tg_group_id']}")


def test_team_funcs():
    initial_teams = client.get("/teams")

    team = {"team_name": "sustem inc", "members": ['Boris', 'Timofei', 'Stepan', 'Nikita'], "tg_group_id": 'idkwhichnumber'}

    # Add new team to firestore
    response = client.post("/team", json=team)
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

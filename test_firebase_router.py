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

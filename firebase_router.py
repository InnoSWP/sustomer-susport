import uvicorn
from fastapi import FastAPI, Response
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from pydantic.class_validators import Union
from pydantic.fields import Optional, Field

from firebase.firestore_database import FirestoreDatabase
from firebase.team_entry import TeamEntry
from firebase.chat_entry import ChatEntry

app = FastAPI()
fd = FirestoreDatabase(app_name="firebase_router")


class TeamItem(BaseModel):
    team_name: str
    tg_group_id: int
    members: Optional[list[Union[int, str]]] = Field(None)


@app.get("/", status_code=404)
def index():
    return Response(status_code=404)


@app.get("/teams")
def get_teams():
    cur_teams = fd.teams()

    answer = [{"team_name": t.team_name, "members": t.members, "tg_group_id": t.tg_group_id} for t in cur_teams]
    return answer


@app.get("/team")
def get_team(team_name: str):
    cur_teams = fd.teams()

    answer = [{"team_name": t.team_name, "members": t.members, "tg_group_id": t.tg_group_id}
              for t in cur_teams if t.team_name == team_name]
    if answer:
        return answer[0]
    else:
        return JSONResponse({"status": "Team with such name does not exist"}, status_code=404)


@app.post("/new-team")
def set_team(t_item: TeamItem):
    # Check teams with the same name
    cur_teams = fd.teams()
    already_exist = bool([t for t in cur_teams if t.team_name == t_item.team_name])

    if not already_exist:
        team_entry = TeamEntry(t_item.team_name, t_item.tg_group_id, t_item.members)
        fd.set_team(team_entry)
        return Response(status_code=201)
    else:
        return JSONResponse({"status": "Team with such name already exists"}, status_code=409)


@app.delete("/delete-team")
def delete_question(team_name: str):
    # Check if such team exists
    cur_teams = fd.teams()
    already_exist = bool([t for t in cur_teams if t.team_name == team_name])

    if not already_exist:
        return JSONResponse({"status": "Team with such name does not exist"}, status_code=404)

    fd.delete_team(team_name)

    return Response(status_code=200)


def run_router():
    uvicorn.run(app, port=8000)


if __name__ == "__main__":
    run_router()

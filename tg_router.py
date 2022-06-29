from datetime import datetime

import uvicorn
from fastapi import FastAPI, Response
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from pydantic.class_validators import Union
from pydantic.fields import Field, Optional

from firebase.chat_entry import ChatEntry, ChatMessage
from firebase.firestore_database import FirestoreDatabase
from firebase.team_entry import TeamEntry

app = FastAPI()
fd = FirestoreDatabase(app_name="firebase_router")


class TeamItem(BaseModel):
    team_name: str
    tg_group_id: int
    members: Optional[list[Union[int, str]]] = Field([])


class MessageItem(BaseModel):
    message: str
    user_sent: Optional[bool] = Field(True)
    time: Optional[datetime] = Field(None)


class ChatItem(BaseModel):
    chat_id: str
    is_open: bool
    messages: Optional[list[MessageItem]] = Field([])


@app.get("/", status_code=404)
def index():
    return Response(status_code=404)


@app.get("/teams")
def get_teams():
    cur_teams = fd.teams()

    answer = [t.to_dict() for t in cur_teams]
    return answer


@app.get("/team")
def get_team(team_name: str):
    cur_teams = fd.teams()

    answer = [t.to_dict() for t in cur_teams if t.team_name == team_name]
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
        return JSONResponse(team_entry.to_dict() | {"status": "created"}, status_code=201)
    else:
        return JSONResponse({"status": "Team with such name already exists"}, status_code=409)


@app.delete("/delete-team")
def delete_team(team_name: str):
    # Check if such team exists
    cur_teams = fd.teams()
    already_exist = bool([t for t in cur_teams if t.team_name == team_name])

    if not already_exist:
        return JSONResponse({"status": "Team with such name does not exist"}, status_code=404)

    t = fd.get_team(team_name)
    fd.delete_team(team_name)

    return JSONResponse(t.to_dict() | {"status": "deleted"}, status_code=200)


@app.get("/chats")
def get_chats():
    cur_chats = fd.chats()

    answer = [c.to_dict() for c in cur_chats]
    return answer


@app.get("/chat")
def get_chat(chat_id: str):
    cur_chats = fd.chats()

    answer = [c.to_dict() for c in cur_chats if c.chat_id == chat_id]
    if answer:
        return answer[0]
    else:
        return JSONResponse({"status": "Chat with such ID does not exist"}, status_code=404)


@app.post("/new-chat", status_code=201)
def set_chat(c_item: ChatItem):
    # Check teams with the same name
    cur_chats = fd.chats()
    already_exist = bool([c for c in cur_chats if c.chat_id == c_item.chat_id])

    if not already_exist:
        chat_entry = ChatEntry(c_item.chat_id,
                               is_open=c_item.is_open,
                               messages=[ChatMessage(m.message, time=m.time, user_sent=m.user_sent)
                                         for m in c_item.messages])
        fd.set_chat(chat_entry)
        return chat_entry.to_dict() | {"status": "created"}
    else:
        return JSONResponse({"status": "Chat with such ID already exists"}, status_code=409)


@app.delete("/delete-chat", status_code=200)
def delete_chat(chat_id: str):
    # Check if such team exists
    cur_chats = fd.chats()
    already_exist = bool([c for c in cur_chats if c.chat_id == chat_id])

    if not already_exist:
        return JSONResponse({"status": "Chat with such ID does not exist"}, status_code=404)

    c = fd.get_chat(chat_id)
    fd.delete_chat(chat_id)

    return c.to_dict() | {"status": "deleted"}


def run_router():
    uvicorn.run(app, port=8000)


if __name__ == "__main__":
    run_router()

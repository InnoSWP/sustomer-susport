from datetime import datetime
from json import loads
from os import environ

import firebase_admin
from firebase_admin import credentials, firestore

from firebase.question_entry import QuestionEntry
from firebase.team_entry import TeamEntry
from firebase.chat_entry import ChatEntry, ChatMessage


class FirestoreDatabase:
    def __init__(self, key: str = None, app_name: str = "default"):
        # Search for key in environment
        if not key:
            key = environ.get('firebase_key', 'firebase_key.json')

        # Check if it is a path or json data
        if key[-5:] != '.json':
            key = loads(key)

        cred = credentials.Certificate(key)
        app = firebase_admin.initialize_app(cred, name=app_name)
        self.db = firestore.client(app)

    def teams(self):
        teams_ref = self.db.collection(u'teams')
        docs = teams_ref.stream()

        teams: list[TeamEntry] = [TeamEntry(doc.id,
                                            doc.to_dict()['tg_group_id'],
                                            set(doc.to_dict()['members'])) for doc in docs]

        return teams

    def get_team(self, team: (str, TeamEntry)):
        doc_ref = self.db.collection(u'teams').document(str(team))
        doc = doc_ref.get()

        if doc.exists:
            doc_dict = doc.to_dict()
            return TeamEntry(str(team), doc_dict['tg_group_id'], set(doc_dict['members']))
        else:
            return None

    def set_team(self, team: TeamEntry):
        doc_ref = self.db.collection(u'teams').document(str(team))
        team_data = {u'members': team.members, u'tg_group_id': team.tg_group_id}

        doc_ref.set(team_data)

    def delete_team(self, team: (str, TeamEntry)):
        doc_ref = self.db.collection(u'teams').document(str(team))
        doc_ref.delete()

    def questions(self):
        questions_ref = self.db.collection(u'questions')
        questions_list = questions_ref.get()

        questions: list[QuestionEntry] = []
        for q_item in questions_list:
            q = q_item.to_dict()
            questions.append(QuestionEntry(q['key'], q['question'], q['answer']))

        return questions

    # Returns question item if found exactly same question (question field), otherwise None
    def get_question(self, question: (str, QuestionEntry)):
        questions_ref = self.db.collection(u'questions')
        questions_query = questions_ref.where(u'question', u'==', str(question)).stream()
        q_item = None
        for q_item in questions_query:
            pass

        if q_item:
            question_dict = q_item.to_dict()
            return QuestionEntry(question_dict['key'], question_dict['question'], question_dict['answer'])
        else:
            return None

    def set_question(self, question: QuestionEntry):
        self.db.collection(u'questions').document().set(question.to_dict())

    def delete_question(self, question: (str, QuestionEntry)):
        questions_ref = self.db.collection(u'questions')
        questions_query = questions_ref.where(u'question', u'==', str(question)).stream()
        for q_item in questions_query:
            q_item.reference.delete()

    def chats(self):
        chats_list = self.db.collection(u"chats").get()
        chats = []

        for chat_doc in chats_list:
            c_item = chat_doc.to_dict()
            chats.append(ChatEntry(chat_doc.id, messages=[ChatMessage(m["message"], m["user_sent"], m["time"])
                                                          for m in c_item["messages"]], is_open=c_item["is_open"]))

        return chats

    def get_chat(self, chat_id: (str, ChatEntry)):
        doc_ref = self.db.collection(u'chats').document(str(chat_id))
        doc = doc_ref.get()

        if doc.exists:
            doc_dict = doc.to_dict()
            return ChatEntry(str(chat_id),
                             messages=[ChatMessage(m["message"], m["user_sent"], m["time"])
                                       for m in doc_dict['messages']],
                             is_open=doc_dict['is_open'])
        else:
            return None

    def set_chat(self, chat_entry: ChatEntry):
        doc_ref = self.db.collection(u'chats').document(chat_entry.chat_id)
        team_data = {u'messages': [m.to_dict() for m in chat_entry.messages], u'is_open': chat_entry.is_open}

        doc_ref.set(team_data)

    def delete_chat(self, chat_entry: (str, ChatEntry)):
        doc_ref = self.db.collection(u'chats').document(str(chat_entry))
        doc_ref.delete()

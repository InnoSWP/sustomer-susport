from json import loads
from os import environ

import firebase_admin
from firebase_admin import credentials, firestore
from firebase.question_entry import QuestionEntry
from firebase.team_entry import TeamEntry


class FirestoreDatabase:
    def __init__(self, key: str = None, app_name: str = "default"):
        if not key:
            key_str = environ.get('firebase_key', 'default_value')
            key = loads(key_str)

        cred = credentials.Certificate(key)
        app = firebase_admin.initialize_app(cred, name=app_name)
        self.db = firestore.client(app)

    def teams(self):
        teams_ref = self.db.collection(u'teams')
        docs = teams_ref.stream()

        teams: list[TeamEntry] = [TeamEntry(doc.id, set(doc.to_dict()['members'])) for doc in docs]

        return teams

    def get_team(self, team: (str, TeamEntry)):
        doc_ref = self.db.collection(u'teams').document(str(team))
        doc = doc_ref.get()

        if doc.exists:
            return TeamEntry(str(team), set(doc.to_dict()['members']))
        else:
            return None

    def set_team(self, team: TeamEntry):
        doc_ref = self.db.collection(u'teams').document(str(team))
        team_data = {u'members': team.members}

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
        question_data = {'key': question.key,
                         'question': question.question,
                         'answer': question.answer}
        self.db.collection(u'questions').document().set(question_data)

    def delete_question(self, question: (str, QuestionEntry)):
        questions_ref = self.db.collection(u'questions')
        questions_query = questions_ref.where(u'question', u'==', str(question)).stream()
        for q_item in questions_query:
            q_item.reference.delete()

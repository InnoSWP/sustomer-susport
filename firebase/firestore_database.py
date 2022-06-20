import firebase_admin
from firebase_admin import credentials, firestore

from question_entry import QuestionEntry
from team_entry import TeamEntry


class FirestoreDatabase:
    def __init__(self, path_to_key: str):
        cred = credentials.Certificate(path_to_key)
        firebase_admin.initialize_app(cred)
        self.db = firestore.client()

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
        questions_ref = self.db.collection(u'questions').document(u'keys')
        questions_dict = questions_ref.get().to_dict()

        questions: list[QuestionEntry] = [QuestionEntry(key, questions_dict[key][0], questions_dict[key][1])
                                          for key in questions_dict]

        return questions

    # Returns answer if found exactly the same key
    def get_answer(self, question_key: (str, QuestionEntry)):
        question_ref = self.db.collection(u'questions').document(u'keys')
        question_dic = question_ref.get().to_dict()

        answer = question_dic.get(str(question_key), None)
        if answer:
            return answer[1]
        else:
            return None

    def set_question(self, question: QuestionEntry):
        question_ref = self.db.collection(u'questions').document(u'keys')
        question_data = {question.key: [question.question, question.answer]}

        question_ref.update(question_data)

    def delete_question(self, question: (str, QuestionEntry)):
        question_ref = self.db.collection(u'questions').document(u'keys')
        question_data = {str(question): firestore.DELETE_FIELD}

        question_ref.update(question_data)

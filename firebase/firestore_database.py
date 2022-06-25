import firebase_admin
from firebase_admin import credentials, firestore

from firebase.question_entry import QuestionEntry
from firebase.team_entry import TeamEntry


class FirestoreDatabase:
    def __init__(self, key: str):
        cred = credentials.Certificate('sustomer-susport-private-key.json')
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
        questions_ref = self.db.collection(u'questions')
        questions_list = questions_ref.get()

        questions: list[QuestionEntry] = []
        for q_item in questions_list:
            q = q_item.to_dict()
            questions.append(QuestionEntry(q['key'], q['question'], q['answer']))

        return questions

    # Returns answer if found exactly the same key
    '''
    def get_answer(self, question_key: (str, QuestionEntry)):
        pass
    '''

    def set_question(self, question: QuestionEntry):
        question_data = {'key': question.key,
                         'question': question.question,
                         'answer': question.answer}
        self.db.collection(u'questions').document().set(question_data)

    '''
    def delete_question(self, question: (str, QuestionEntry)):
        pass
    '''

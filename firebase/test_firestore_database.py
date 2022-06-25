from firestore_database import FirestoreDatabase
from team_entry import TeamEntry
from question_entry import QuestionEntry


class TestFirestoreDatabase:
    fd = FirestoreDatabase()

    def test_teams(self):
        for t in self.fd.teams():
            print(f'{t.team_name}: {t.members}')

    def test_team_funcs(self):
        initial_teams = self.fd.teams()

        team_1 = TeamEntry("team_1_OAIwnn2238FFew331u")
        team_2 = TeamEntry("team_2_OAIwnn2238FFew331u", set())
        team_3 = TeamEntry("team_3_OAIwnn2238FFew331u", {"@user_1", 228, "@user_3"})

        self.fd.set_team(team_1)
        self.fd.set_team(team_2)
        self.fd.set_team(team_3)

        assert self.fd.teams() != initial_teams

        assert self.fd.get_team(team_1) == team_1
        assert self.fd.get_team(team_2) == team_2
        assert self.fd.get_team("team_3_OAIwnn2238FFew331u") == team_3
        assert self.fd.get_team("none_existing_team_OAIwnn2238FFew331u") is None

        self.fd.delete_team(team_1)
        self.fd.delete_team(team_2)
        self.fd.delete_team("team_3_OAIwnn2238FFew331u")

        assert self.fd.teams() == initial_teams

    def test_questions(self):
        for q in self.fd.questions():
            print(f"{q.question}: {q.answer}")

    def test_question_funcs(self):
        initial_questions = self.fd.questions()

        question_1 = QuestionEntry("key_1", "What is the hottest planet in our system?", "Venus")
        question_2 = QuestionEntry("key_2", "What does the fox say?", "Mimmimimimmimii")
        question_3 = QuestionEntry("key_3", "Why were you running away?", "Why were you pursuing me?")

        self.fd.set_question(question_1)
        self.fd.set_question(question_2)
        self.fd.set_question(question_3)

        assert self.fd.questions() != initial_questions

        assert self.fd.get_question(question_1) == question_1
        assert self.fd.get_question(question_2) == question_2
        assert self.fd.get_question("Why were you running away?") == question_3
        assert self.fd.get_question("Non-existing question_OAIwnn2238FFew331u") is None

        self.fd.delete_question(question_1)
        self.fd.delete_question(question_2)
        self.fd.delete_question("Why were you running away?")

        assert self.fd.questions() == initial_questions

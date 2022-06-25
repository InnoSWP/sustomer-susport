from firestore_database import FirestoreDatabase


class TestFirestoreDatabase:
    fd = FirestoreDatabase()

    def test_teams(self):
        for t in self.fd.teams():
            print(f'{t.team_name}: {t.members}')

    def test_get_team(self):
        assert False

    def test_set_team(self):
        assert False

    def test_delete_team(self):
        assert False

    def test_questions(self):
        for q in self.fd.questions():
            print(f"{q.question}: {q.answer}")

    def test_set_question(self):
        assert False

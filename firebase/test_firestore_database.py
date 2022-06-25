from firestore_database import FirestoreDatabase
from os import environ


def test_teams():
    firebase_key = environ.get('firebase_key', 'default_value')
    fd = FirestoreDatabase(firebase_key)
    for t in fd.teams():
        print(f'{t.team_name}: {t.members}')


def test_get_team():
    assert False


def test_set_team():
    assert False


def test_delete_team():
    assert False


def test_questions():
    assert False


def test_set_question():
    assert False

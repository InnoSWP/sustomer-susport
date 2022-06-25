from os import environ


def test_teams():
    firebase_key = environ.get('firebase_key', 'default_value')
    print(firebase_key)
    assert False


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

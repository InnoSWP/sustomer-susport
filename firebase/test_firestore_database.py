import pytest


@pytest.fixture(scope="session")
def firebase_key(pytestconfig):
    return pytestconfig.getoption("firebase_key")


def test_teams(firebase_key):
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

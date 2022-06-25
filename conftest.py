def pytest_addoption(parser):
    parser.addoption("--firebase_key", action="store", default="")

import pytest


@pytest.fixture
def slqlite():
    return {"PATH": "db.sqlite"}

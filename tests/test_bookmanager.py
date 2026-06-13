"""Smoke tests for the book manager covering the create/read/update/delete flow.

I point the app at a throwaway SQLite database before importing it so the tests
never touch my real bookdatabase.db.
"""

import os
import tempfile

os.environ["DATABASE_URL"] = f"sqlite:///{os.path.join(tempfile.mkdtemp(), 'test.db')}"

import pytest  # noqa: E402

import bookmanager  # noqa: E402


@pytest.fixture
def client():
    # Start each test from an empty table so the assertions are independent.
    with bookmanager.app.app_context():
        bookmanager.db.drop_all()
        bookmanager.db.create_all()
    return bookmanager.app.test_client()


def titles_on_page(response):
    body = response.get_data(as_text=True)
    return [line.strip() for line in body.splitlines() if line.strip() in {"Dune", "1984"}]


def test_list_starts_empty(client):
    response = client.get("/")
    assert response.status_code == 200
    assert titles_on_page(response) == []


def test_add_book(client):
    response = client.post("/", data={"title": "Dune"})
    assert response.status_code == 200
    assert "Dune" in titles_on_page(response)


def test_update_book(client):
    client.post("/", data={"title": "Dune"})
    client.post("/update", data={"old_title": "Dune", "new_title": "1984"})
    response = client.get("/")
    assert "1984" in titles_on_page(response)
    assert "Dune" not in titles_on_page(response)


def test_delete_book(client):
    client.post("/", data={"title": "Dune"})
    client.post("/delete", data={"title": "Dune"})
    response = client.get("/")
    assert titles_on_page(response) == []

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from app import app


def test_index():
    response = app.test_client().get("/")

    assert response.status_code == 200
    assert response.get_json()["status"] == "online"


def test_fetch_existing_pokefruit():
    response = app.test_client().get("/fetch/5048ba4b0d704e38a4b1b446ad199fd6")

    assert response.status_code == 200
    assert response.get_json()["name"] == "Bananachu"


def test_fetch_unknown_pokefruit():
    response = app.test_client().get("/fetch/codigo-inexistente")

    assert response.status_code == 200
    payload = response.get_json()
    assert payload["code"] == "codigo-inexistente"
    assert payload["generated"] is True
    assert payload["name"]


def test_unknown_code_reuses_same_pokefruit():
    client = app.test_client()
    first = client.get("/fetch/codigo-reabertura").get_json()
    second = client.get("/fetch/codigo-reabertura").get_json()

    assert first["name"] == second["name"]


def test_database_has_no_duplicate_names_or_codes():
    from app import load_database

    items = load_database()
    assert len(items) == len({item["code"] for item in items})
    assert len(items) == len({item["name"].lower() for item in items})

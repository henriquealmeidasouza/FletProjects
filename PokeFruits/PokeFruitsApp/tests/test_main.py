import sys
import importlib
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parents[1] / "src"))

view = importlib.import_module("view")


def test_generate_unique_code_has_expected_prefix():
    code = view.generate_unique_code()

    assert code.startswith("CPDOG-")
    assert len(code) == 18


def test_fetch_pokefruit_data_uses_server(monkeypatch):
    expected = {"code": "5048ba4b0d704e38a4b1b446ad199fd6", "name": "Bananachu"}

    class Response:
        status_code = 200

        def raise_for_status(self):
            return None

        def json(self):
            return expected

    monkeypatch.setattr(view.requests, "get", lambda *args, **kwargs: Response())
    monkeypatch.setattr(view, "save_pokefruit_data", lambda code, payload: None)

    assert view.fetch_pokefruit_data(expected["code"]) == expected


def test_fetch_pokefruit_data_returns_generated_pokefruit(monkeypatch):
    expected = {
        "code": "codigo-inexistente",
        "name": "Pearas",
        "generated": True,
    }

    class Response:
        status_code = 200

        def raise_for_status(self):
            return None

        def json(self):
            return expected

    monkeypatch.setattr(view.requests, "get", lambda *args, **kwargs: Response())
    monkeypatch.setattr(view, "save_pokefruit_data", lambda code, payload: None)

    assert view.fetch_pokefruit_data("codigo-inexistente") == expected


def test_fetch_pokefruit_data_returns_local_pokefruit_on_404(monkeypatch):
    class Response:
        status_code = 404

        def raise_for_status(self):
            return None

    monkeypatch.setattr(view.requests, "get", lambda *args, **kwargs: Response())
    monkeypatch.setattr(view, "save_pokefruit_data", lambda code, payload: None)

    payload = view.fetch_pokefruit_data("codigo-novo")

    assert payload["code"] == "codigo-novo"
    assert payload["generated"] is True
    assert payload["name"] in {"Bananachu", "Pearas"}


def test_saved_pokefruit_appears_in_local_database(tmp_path, monkeypatch):
    monkeypatch.setenv("FLET_APP_STORAGE_DATA", str(tmp_path))

    database = importlib.import_module("database")

    database.save_pokefruit_data(
        "CPDOG-LISTA",
        {"code": "CPDOG-LISTA", "name": "Bananachu"},
    )

    saved = database.list_saved_pokefruits()

    assert {"code": "CPDOG-LISTA", "name": "Bananachu"} in saved

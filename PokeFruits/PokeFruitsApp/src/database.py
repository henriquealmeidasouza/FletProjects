import json
import os
import sqlite3


def _db_path():
    base_dir = os.environ.get(
        "FLET_APP_STORAGE_DATA",
        os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "src", "data"),
    )
    os.makedirs(base_dir, exist_ok=True)
    return os.path.join(base_dir, "pokefruit.db")


def _connect():
    return sqlite3.connect(_db_path())


def init_db():
    with _connect() as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS pokefruit_data (
                code TEXT PRIMARY KEY,
                payload TEXT NOT NULL,
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
            )
            """
        )


def save_pokefruit_data(code: str, payload: dict):
    if not code or not payload:
        return
    init_db()
    with _connect() as conn:
        conn.execute(
            """
            INSERT INTO pokefruit_data (code, payload)
            VALUES (?, ?)
            ON CONFLICT(code) DO UPDATE SET payload = excluded.payload
            """,
            (code.strip(), json.dumps(payload, ensure_ascii=False)),
        )


def get_pokefruit_data(code: str):
    if not code:
        return None
    init_db()
    with _connect() as conn:
        row = conn.execute(
            "SELECT payload FROM pokefruit_data WHERE code = ?",
            (code.strip(),),
        ).fetchone()
    if row is None:
        return None
    try:
        return json.loads(row[0])
    except (TypeError, ValueError):
        return None


def list_saved_pokefruits():
    init_db()
    with _connect() as conn:
        rows = conn.execute(
            "SELECT code, payload FROM pokefruit_data ORDER BY created_at DESC, code ASC"
        ).fetchall()

    saved = []
    for code, payload_json in rows:
        try:
            payload = json.loads(payload_json)
        except (TypeError, ValueError):
            payload = {}
        saved.append({
            "code": code,
            "name": payload.get("name", "Pokefruit"),
        })
    return saved


class PokeFruitDatabase:
    def __init__(self, database_path: str | None = None):
        if database_path is None:
            database_path = _db_path()
        self.database_path = database_path
        self._initialize()

    def _connect(self):
        return sqlite3.connect(self.database_path)

    def _initialize(self):
        directory = os.path.dirname(self.database_path)
        if directory:
            os.makedirs(directory, exist_ok=True)
        with self._connect() as connection:
            connection.execute(
                """
                CREATE TABLE IF NOT EXISTS pokefruits (
                    code TEXT PRIMARY KEY,
                    data TEXT NOT NULL,
                    updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
                )
                """
            )

    def save(self, pokefruit: dict) -> None:
        code = pokefruit.get("code")
        if not isinstance(code, str) or not code.strip():
            raise ValueError("O Pokefruit não contém um código válido.")
        with self._connect() as connection:
            connection.execute(
                """
                INSERT INTO pokefruits (code, data, updated_at)
                VALUES (?, ?, CURRENT_TIMESTAMP)
                ON CONFLICT(code) DO UPDATE SET
                    data = excluded.data,
                    updated_at = CURRENT_TIMESTAMP
                """,
                (code, json.dumps(pokefruit, ensure_ascii=False)),
            )

    def get(self, code: str) -> dict | None:
        with self._connect() as connection:
            row = connection.execute(
                "SELECT data FROM pokefruits WHERE code = ?", (code,),
            ).fetchone()
        return json.loads(row[0]) if row else None


init_db()

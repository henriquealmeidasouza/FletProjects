import json
import os
import sqlite3


def _db_path():
    base_dir = os.environ.get(
        "FLET_APP_STORAGE_DATA",
        os.path.join(os.path.expanduser("~"), ".pokefruit"),
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


init_db()

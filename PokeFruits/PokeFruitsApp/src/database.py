import json
import os
import sqlite3


class PokeFruitDatabase:
    def __init__(self, database_path: str | None = None):
        if database_path is None:
            app_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            database_path = os.path.join(app_dir, "pokefruits.sqlite3")
        self.database_path = database_path
        self._initialize()

    def _connect(self):
        return sqlite3.connect(self.database_path)

    def _initialize(self):
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
                "SELECT data FROM pokefruits WHERE code = ?",
                (code,),
            ).fetchone()

        return json.loads(row[0]) if row else None

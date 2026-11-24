import os
import json
import random
from copy import deepcopy
from flask import Flask, jsonify

app = Flask(__name__)
WD = os.path.dirname(os.path.abspath(__file__))


def load_database() -> list[dict]:
    path = os.path.join(WD, "data.json")
    with open(path, "r", encoding="utf-8") as data_file:
        data = json.load(data_file)
    if not isinstance(data, list):
        raise ValueError("O arquivo data.json deve conter uma lista de Pokefruits.")

    unique = []
    seen_codes = set()
    seen_names = set()
    for pokemon in data:
        code = str(pokemon.get("code", "")).strip()
        name = str(pokemon.get("name", "")).strip().lower()
        if not code or code in seen_codes or name in seen_names:
            continue
        seen_codes.add(code)
        seen_names.add(name)
        unique.append(pokemon)
    return unique


ASSIGNMENTS_PATH = os.path.join(WD, "generated_assignments.json")


def load_assignments() -> dict:
    if not os.path.exists(ASSIGNMENTS_PATH):
        return {}
    with open(ASSIGNMENTS_PATH, "r", encoding="utf-8") as data_file:
        assignments = json.load(data_file)
    return assignments if isinstance(assignments, dict) else {}


def save_assignments(assignments: dict):
    with open(ASSIGNMENTS_PATH, "w", encoding="utf-8") as data_file:
        json.dump(assignments, data_file, ensure_ascii=False, indent=2)


@app.route("/", methods=["GET"])
def index():
    return jsonify({"name": "PokeFruits API", "status": "online"})


@app.route("/fetch/<code>", methods=["GET"])
def fetch_pokefruit(code: str):
    code = code.strip()
    if not code:
        return jsonify({"error": "Código não informado."}), 400

    database = load_database()

    for pokemon in database:
        if pokemon.get("code") == code:
            return jsonify(pokemon)

    if not database:
        return jsonify({"error": "Nenhum Pokefruit disponível."}), 404

    assignments = load_assignments()

    if code in assignments:
        assigned_code = assignments[code]
        for pokemon in database:
            if pokemon.get("code") == assigned_code:
                result = deepcopy(pokemon)
                result["code"] = code
                result["generated"] = True
                return jsonify(result)

    used_codes = set(assignments.values())
    available = [pokemon for pokemon in database if pokemon.get("code") not in used_codes]
    if not available:
        return jsonify({"error": "Todos os Pokefruits já foram utilizados."}), 409

    pokemon = deepcopy(random.choice(available))
    assignments[code] = pokemon["code"]
    save_assignments(assignments)

    pokemon["code"] = code
    pokemon["id"] = None
    pokemon["generated"] = True
    return jsonify(pokemon)


@app.errorhandler(FileNotFoundError)
def handle_missing_database(error):
    return jsonify({"error": "Base de dados não encontrada."}), 500


@app.errorhandler(json.JSONDecodeError)
@app.errorhandler(ValueError)
def handle_invalid_database(error):
    return jsonify({"error": "Base de dados inválida."}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
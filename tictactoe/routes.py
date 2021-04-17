"""JSON game endpoints and page routes."""
from flask import Blueprint, jsonify, session, request
from .service import new_game, take_turn

bp = Blueprint("game", __name__)


def current_game():
    if "game" not in session:
        session["game"] = new_game()
    return session["game"]


@bp.get("/api/game")
def get_game():
    return jsonify(current_game())


def json_object():
    data = request.get_json(silent=True)
    if not isinstance(data, dict):
        raise ValueError("Send a JSON object.")
    return data


@bp.post("/api/new")
def start_game():
    data = json_object()
    human = data.get("human", "X")
    if human not in ("X", "O"):
        raise ValueError("Choose X or O.")
    reset = data.get("reset_scores", False)
    if type(reset) is not bool:
        raise ValueError("reset_scores must be true or false.")
    scores = None if reset else current_game()["scores"]
    session["game"] = new_game(human, scores)
    return jsonify(session["game"])


@bp.post("/api/move")
def move():
    data = json_object()
    game = take_turn(current_game(), data.get("index"))
    session["game"] = game
    return jsonify(game)

"""JSON game endpoints and page routes."""
import secrets
from flask import Blueprint, jsonify, session, request
from .service import new_game, take_turn

bp = Blueprint("game", __name__)


def current_game():
    if "game" not in session:
        session["game"] = new_game()
    return session["game"]


@bp.get("/api/game")
def get_game():
    game = dict(current_game())
    if "csrf_token" not in session:
        session["csrf_token"] = secrets.token_hex(32)
    game["csrf_token"] = session["csrf_token"]
    return jsonify(game)


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


@bp.before_request
def check_token():
    if request.method == "POST":
        token = session.get("csrf_token")
        supplied = request.headers.get("X-CSRF-Token", "")
        if not token or not secrets.compare_digest(token, supplied):
            return jsonify(error="Session expired. Reload the page and try again."), 403


@bp.app_errorhandler(ValueError)
def invalid_move(error):
    return jsonify(error=str(error)), 400


@bp.app_errorhandler(413)
def too_large(error):
    return jsonify(error="Request is too large."), 413


@bp.after_request
def no_cache(response):
    if request.path.startswith("/api/"):
        response.headers["Cache-Control"] = "no-store"
    return response

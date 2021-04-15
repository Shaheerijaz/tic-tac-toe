"""JSON game endpoints and page routes."""
from flask import Blueprint, jsonify, session
from .service import new_game

bp = Blueprint("game", __name__)


def current_game():
    if "game" not in session:
        session["game"] = new_game()
    return session["game"]


@bp.get("/api/game")
def get_game():
    return jsonify(current_game())

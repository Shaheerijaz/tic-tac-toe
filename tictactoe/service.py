"""Round orchestration, independent of HTTP."""
from dataclasses import asdict
from .ai import SearchStats, best_move
from .game import new_board, opponent, outcome, play_move, winning_line


def computer_turn(game):
    stats = SearchStats()
    ai = opponent(game["human"])
    move = best_move(game["board"], ai, stats)
    if move is not None:
        game["board"] = play_move(game["board"], move, ai)
    game["stats"] = asdict(stats)
    game["last_ai_move"] = move


def new_game(human="X", scores=None):
    opponent(human)
    game = {"board": new_board(), "human": human, "result": None,
            "winning_line": [], "last_ai_move": None,
            "stats": asdict(SearchStats()),
            "scores": dict(scores or {"human": 0, "ai": 0, "draw": 0})}
    if human == "O":
        computer_turn(game)
    return game


def take_turn(game, index):
    game["board"] = play_move(game["board"], index, game["human"])
    if outcome(game["board"]) is None:
        computer_turn(game)
    game["result"] = outcome(game["board"])
    game["winning_line"] = winning_line(game["board"])
    if game["result"] is not None:
        key = ("draw" if game["result"] == "draw" else
               "human" if game["result"] == game["human"] else "ai")
        game["scores"][key] += 1
    return game

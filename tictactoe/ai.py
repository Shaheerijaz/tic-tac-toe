"""Depth-aware minimax from the computer player's perspective."""
from math import inf
from .game import available_moves, next_player, opponent, outcome, validate_board


def minimax(board, turn, ai, depth=0):
    result = outcome(board)
    if result is not None:
        return 0 if result == "draw" else (10 - depth if result == ai else depth - 10)
    scores = []
    for index in available_moves(board):
        child = board.copy()
        child[index] = turn
        scores.append(minimax(child, opponent(turn), ai, depth + 1))
    return max(scores) if turn == ai else min(scores)


def best_move(board, ai):
    validate_board(board)
    opponent(ai)
    if outcome(board) is not None:
        return None
    if next_player(board) != ai:
        raise ValueError("The computer cannot move out of turn.")
    best, choice = -inf, None
    for index in available_moves(board):
        child = board.copy()
        child[index] = ai
        score = minimax(child, opponent(ai), ai, 1)
        if score > best:
            best, choice = score, index
    return choice

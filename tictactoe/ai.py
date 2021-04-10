"""Depth-aware minimax from the computer player's perspective."""
from math import inf
from .game import next_player, opponent, outcome, validate_board


# Center, corners, then edges make pruning more effective and ties stable.
MOVE_ORDER = (4, 0, 2, 6, 8, 1, 3, 5, 7)


def ordered_moves(board):
    return [index for index in MOVE_ORDER if not board[index]]


def minimax(board, turn, ai, depth=0, alpha=-inf, beta=inf):
    result = outcome(board)
    if result is not None:
        return 0 if result == "draw" else (10 - depth if result == ai else depth - 10)
    maximizing = turn == ai
    value = -inf if maximizing else inf
    for index in ordered_moves(board):
        child = board.copy()
        child[index] = turn
        score = minimax(child, opponent(turn), ai, depth + 1, alpha, beta)
        if maximizing:
            value = max(value, score)
            alpha = max(alpha, value)
        else:
            value = min(value, score)
            beta = min(beta, value)
        if alpha >= beta:
            break
    return value


def best_move(board, ai):
    validate_board(board)
    opponent(ai)
    if outcome(board) is not None:
        return None
    if next_player(board) != ai:
        raise ValueError("The computer cannot move out of turn.")
    best, choice = -inf, None
    for index in ordered_moves(board):
        child = board.copy()
        child[index] = ai
        score = minimax(child, opponent(ai), ai, 1)
        if score > best:
            best, choice = score, index
    return choice

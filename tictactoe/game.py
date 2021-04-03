"""Pure Tic Tac Toe rules; cells use X, O, or an empty string."""
EMPTY = ""
MARKS = ("X", "O")


def new_board():
    return [EMPTY] * 9


def opponent(mark):
    if mark not in MARKS:
        raise ValueError("Choose X or O.")
    return "O" if mark == "X" else "X"


def available_moves(board):
    return [index for index, cell in enumerate(board) if cell == EMPTY]

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


WIN_LINES = (
    (0, 1, 2), (3, 4, 5), (6, 7, 8),
    (0, 3, 6), (1, 4, 7), (2, 5, 8),
    (0, 4, 8), (2, 4, 6),
)


def winning_line(board):
    for line in WIN_LINES:
        a, b, c = line
        if board[a] and board[a] == board[b] == board[c]:
            return list(line)
    return []


def outcome(board):
    """Return X, O, draw, or None for an unfinished game."""
    line = winning_line(board)
    if line:
        return board[line[0]]
    return "draw" if not available_moves(board) else None


def validate_board(board):
    if not isinstance(board, list) or len(board) != 9:
        raise ValueError("The board must contain nine cells.")
    if any(cell not in (EMPTY, *MARKS) for cell in board):
        raise ValueError("Cells must be X, O, or empty.")
    xs, os = board.count("X"), board.count("O")
    if xs not in (os, os + 1):
        raise ValueError("Invalid turn counts.")
    winners = {board[a] for a, b, c in WIN_LINES
               if board[a] and board[a] == board[b] == board[c]}
    if len(winners) > 1:
        raise ValueError("Both players cannot win.")
    if ("X" in winners and xs != os + 1) or ("O" in winners and xs != os):
        raise ValueError("Invalid winning position.")


def next_player(board):
    validate_board(board)
    return "X" if board.count("X") == board.count("O") else "O"

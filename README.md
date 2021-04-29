# Three in a row — Flask Tic Tac Toe

A browser game powered by **Flask 2.0.3** and a Python **minimax algorithm with alpha-beta pruning**. Choose X (first) or O (second), play the computer, restart rounds, and track session scores. The interface shows nodes visited, pruning cutoffs, and elapsed search time for the last computer move.

## Run locally

Use Python 3.9 or newer (verified with Python 3.9.6). From this repository:

```sh
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python app.py
```

On Windows, activate with `.venv\Scripts\activate` and use `python` instead of `python3`.

Open http://127.0.0.1:5000. If port 5000 is occupied (including by macOS AirPlay), run:

```sh
PORT=5050 python app.py
```

PowerShell equivalent: `$env:PORT = "5050"; python app.py`.

JavaScript and browser cookies must be enabled. No Node.js, database, API key, external fonts, or frontend build step is needed.

## Play

- Click or keyboard-activate an empty square. The server validates the move and replies with the computer's move.
- X always starts. Selecting O lets the computer open as X.
- New round clears the board and preserves scores; changing symbols also begins a new round.
- Reset clears scores and starts a new round with your current symbol.
- A win highlights the winning three cells. An outline marks the latest computer move.
- Refreshing restores your game. Use Reconnect after a connection failure to read the server's current state.

The computer plays optimally: you can draw, but you cannot beat it from a fresh legal game.

## How the algorithm works

`tictactoe/ai.py` contains the search. Each candidate computer move is evaluated recursively. Computer turns maximize the score; human turns minimize it.

| Terminal result | Score |
| --- | --- |
| Computer wins | `10 - depth` |
| Human wins | `depth - 10` |
| Draw | `0` |

Depth-sensitive scoring prefers faster wins and postpones unavoidable losses. Alpha is the maximizing player's best established lower bound; beta is the minimizing player's best established upper bound. Once `alpha >= beta`, remaining alternatives in that branch cannot change the decision and are skipped. Move ordering considers the center, corners, then edges, improving pruning and making equal-score choices deterministic.

The root evaluates each possible move with a fresh search window. Child searches use copied boards, leaving the caller's board unchanged. Metrics count visited recursive nodes and cutoff events; a cutoff is **not** a count of skipped nodes. Timing measures the server's search, not network latency.

## Tests

```sh
python -m unittest discover -v
python -m pip check
```

The suite covers legal and illegal moves, all eight winning lines, draws, tactical AI choices, independent sessions, JSON validation, CSRF checks, request limits, and score reset behavior. An independent, unpruned, cached minimax oracle checks optimal outcomes for **all 4,520 playable positions** among **5,478 reachable board states**. This verifies the computer's decisions for both symbols, including positions a perfect computer would not ordinarily reach.

## Structure

```text
app.py                   Local server entry point
requirements.txt         Exact runtime versions
tictactoe/__init__.py     Flask application factory and configuration
tictactoe/game.py         Pure game rules and validation
tictactoe/ai.py           Minimax, alpha-beta pruning, search metrics
tictactoe/service.py      Round lifecycle and scoreboard
tictactoe/routes.py       Page and JSON routes
tictactoe/templates/      Jinja page
tictactoe/static/         CSS and vanilla JavaScript
tests/                   Standard-library unittest suite
```

## JSON API

First call `GET /api/game` and retain its session cookie and `csrf_token`. Send that token in the `X-CSRF-Token` header on every POST.

| Method | Path | JSON body |
| --- | --- | --- |
| GET | `/api/game` | None |
| POST | `/api/move` | `{"index": 0}` (indices 0–8, row-major) |
| POST | `/api/new` | `{"human": "O", "reset_scores": false}` |

Successful responses include board, human symbol, result (`null`, `X`, `O`, or `draw`), winning line, last AI move, search statistics, and scores. Invalid game inputs return HTTP 400 with an `error` message, invalid/missing tokens return 403, and oversized bodies return 413. The client sends only the chosen index, never a replacement board.

## Sessions and configuration

The game and scores live in Flask's signed session cookie, so each browser has its own game. The same browser's tabs share that game; use a single active tab for sequential play. This is a local educational game, without accounts or durable storage.

`SECRET_KEY` can be exported in your shell for consistent sessions across restarts. If omitted, the application generates a key on startup, and restarting resets browser sessions. `.env.example` documents the variables; it is not loaded automatically. Set one stable key across workers if adapting the application to a multi-worker server.

The requested [Flask 2.0 release series](https://flask.palletsprojects.com/en/stable/changes/#version-2-0-3) is pinned, together with Werkzeug 2.0.3 and the other dependencies. This project targets local learning; review and upgrade the legacy framework before public deployment. `app.py` binds only to localhost and does not enable debug mode.

## Incremental Git history

This directory is a real Git repository with more than 30 incremental commits: foundation, rules, validation, initial minimax, alpha-beta optimization, search ordering, tests, session service, endpoints, browser interface, exhaustive verification, and documentation. Commits were created in order during development, with their actual timestamps.

```sh
git log --reverse --oneline
git rev-list --count HEAD
git status --short
```

Keep the `.git` directory when copying or extracting the project to preserve that history. No remote repository has been configured or pushed.

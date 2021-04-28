"""Independent unpruned oracle checks every legal nonterminal position."""
import unittest
from functools import lru_cache
from tictactoe.ai import SearchStats, best_move, minimax
from tictactoe.game import available_moves, new_board, opponent, outcome


@lru_cache(maxsize=None)
def oracle(board, turn, ai):
    result = outcome(board)
    if result is not None:
        return 0 if result == "draw" else 1 if result == ai else -1
    values = []
    for index in available_moves(board):
        child = list(board)
        child[index] = turn
        values.append(oracle(tuple(child), opponent(turn), ai))
    return (max if turn == ai else min)(values)


class ExhaustiveTests(unittest.TestCase):
    def test_every_reachable_position_chooses_optimal_outcome(self):
        visited = set()
        checked = 0

        def visit(board, turn):
            nonlocal checked
            key = tuple(board)
            if key in visited:
                return
            visited.add(key)
            if outcome(board) is not None:
                return
            index = best_move(board, turn)
            self.assertIn(index, available_moves(board))
            chosen = board.copy()
            chosen[index] = turn
            self.assertEqual(oracle(tuple(chosen), opponent(turn), turn),
                             oracle(key, turn, turn), (board, turn, index))
            checked += 1
            for move in available_moves(board):
                child = board.copy()
                child[move] = turn
                visit(child, opponent(turn))

        visit(new_board(), "X")
        self.assertEqual(len(visited), 5478)
        self.assertEqual(checked, 4520)
        self.assertEqual(oracle(tuple(new_board()), "X", "X"), 0)
        self.assertEqual(oracle(tuple(new_board()), "X", "O"), 0)

    def test_pruning_reduces_work_and_preserves_draw(self):
        stats = SearchStats()
        self.assertEqual(minimax(new_board(), "X", "X", stats=stats), 0)
        self.assertGreater(stats.cutoffs, 0)
        # An unpruned full Tic Tac Toe tree contains 549,946 nodes.
        self.assertLess(stats.nodes, 549946)

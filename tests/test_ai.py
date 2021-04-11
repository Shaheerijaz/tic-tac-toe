import unittest
from tictactoe.ai import best_move
from tictactoe.game import new_board


class SearchTests(unittest.TestCase):
    def test_takes_immediate_win(self):
        self.assertEqual(best_move(["X", "X", "", "O", "O", "", "X", "", ""], "O"), 5)

    def test_blocks_immediate_loss(self):
        self.assertEqual(best_move(["X", "X", "", "", "O", "", "", "", ""], "O"), 2)

    def test_deterministic_opening_and_no_mutation(self):
        board = new_board()
        self.assertEqual(best_move(board, "X"), 4)
        self.assertEqual(board, new_board())

    def test_terminal_and_out_of_turn(self):
        self.assertIsNone(best_move(list("XOXXOOOXX"), "O"))
        with self.assertRaises(ValueError):
            best_move(new_board(), "O")

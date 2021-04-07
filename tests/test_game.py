import unittest
from tictactoe.game import (WIN_LINES, new_board, outcome, play_move,
                           validate_board, winning_line)


class RulesTests(unittest.TestCase):
    def test_all_winning_lines(self):
        for line in WIN_LINES:
            board = new_board()
            for index in line:
                board[index] = "X"
            self.assertEqual(outcome(board), "X")
            self.assertEqual(winning_line(board), list(line))

    def test_draw(self):
        self.assertEqual(outcome(list("XOXXOOOXX")), "draw")

    def test_move_is_immutable(self):
        board = new_board()
        self.assertEqual(play_move(board, 4, "X")[4], "X")
        self.assertEqual(board, new_board())

    def test_bad_moves(self):
        for index in [-1, 9, True, "4", None, 1.5]:
            with self.assertRaises(ValueError):
                play_move(new_board(), index, "X")
        board = play_move(new_board(), 4, "X")
        with self.assertRaises(ValueError):
            play_move(board, 4, "O")
        with self.assertRaises(ValueError):
            play_move(board, 0, "X")

    def test_invalid_boards(self):
        for board in [[], ["Z"] * 9, list("XXXOOO   "), ["O"] + [""] * 8]:
            with self.assertRaises(ValueError):
                validate_board(board)

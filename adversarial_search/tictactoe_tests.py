# tictactoe_tests.py
# From Classic Computer Science Problems in Python Chapter 8
# Copyright 2018 David Kopec
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import unittest
from typing import List
from minimax import find_best_move
from tictactoe import TTTPiece, TTTBoard
from board import Move


class TTTMinimaxTestCase(unittest.TestCase):
    def test_easy_position(self):
        # win in 1 move
        to_win_easy_position: List[TTTPiece] = [TTTPiece.X, TTTPiece.O, TTTPiece.X,
                                                TTTPiece.X, TTTPiece.E, TTTPiece.O,
                                                TTTPiece.E, TTTPiece.E, TTTPiece.O]
        test_board1: TTTBoard = TTTBoard(to_win_easy_position, TTTPiece.X)
        answer1: Move = find_best_move(test_board1)
        self.assertEqual(answer1, 6)

    def test_block_position(self):
        # must block O's win
        to_block_position: List[TTTPiece] = [TTTPiece.X, TTTPiece.E, TTTPiece.E,
                                             TTTPiece.E, TTTPiece.E, TTTPiece.O,
                                             TTTPiece.E, TTTPiece.X, TTTPiece.O]
        test_board2: TTTBoard = TTTBoard(to_block_position, TTTPiece.X)
        answer2: Move = find_best_move(test_board2)
        self.assertEqual(answer2, 2)

    def test_hard_position(self):
        # find the best move to win 2 moves
        to_win_hard_position: List[TTTPiece] = [TTTPiece.X, TTTPiece.E, TTTPiece.E,
                                                TTTPiece.E, TTTPiece.E, TTTPiece.O,
                                                TTTPiece.O, TTTPiece.X, TTTPiece.E]
        test_board3: TTTBoard = TTTBoard(to_win_hard_position, TTTPiece.X)
        answer3: Move = find_best_move(test_board3)
        self.assertEqual(answer3, 1)

class TTTBoardLogicTestCase(unittest.TestCase):
    def test_legal_moves_empty_board(self):
        # 빈 보드에서는 0~8까지 전부 legal
        empty_position: List[TTTPiece] = [TTTPiece.E] * 9
        board: TTTBoard = TTTBoard(empty_position, TTTPiece.X)

        expected_moves: List[Move] = list(range(9))
        self.assertEqual(board.legal_moves, expected_moves)

    def test_legal_moves_partial_board(self):
        # 일부 칸이 채워진 보드에서 legal_moves가 빈 칸만 반환하는지 확인
        position: List[TTTPiece] = [
            TTTPiece.X, TTTPiece.O, TTTPiece.X,
            TTTPiece.E, TTTPiece.E, TTTPiece.O,
            TTTPiece.E, TTTPiece.X, TTTPiece.E
        ]
        board: TTTBoard = TTTBoard(position, TTTPiece.O)

        # E(빈 칸) 위치: 3, 4, 6, 8
        expected_moves: List[Move] = [3, 4, 6, 8]
        self.assertEqual(sorted(board.legal_moves), expected_moves)

    def test_is_win_rows_cols_diagonals(self):
        # X가 첫 번째 가로줄로 승리한 상태
        winning_position: List[TTTPiece] = [
            TTTPiece.X, TTTPiece.X, TTTPiece.X,
            TTTPiece.E, TTTPiece.O, TTTPiece.E,
            TTTPiece.O, TTTPiece.E, TTTPiece.E
        ]
        board: TTTBoard = TTTBoard(winning_position, TTTPiece.O)

        # is_win 이 현재 보드가 승리 상태인지 나타내는 bool 속성이라고 가정
        self.assertTrue(board.is_win)
        # 승리 상태이므로 무승부는 아님
        self.assertFalse(board.is_draw)

    def test_is_draw_full_board_no_winner(self):
        # 가득 찼지만 어느 쪽도 이기지 않은 무승부 상태
        draw_position: List[TTTPiece] = [
            TTTPiece.X, TTTPiece.O, TTTPiece.X,
            TTTPiece.X, TTTPiece.O, TTTPiece.O,
            TTTPiece.O, TTTPiece.X, TTTPiece.X
        ]
        board: TTTBoard = TTTBoard(draw_position, TTTPiece.X)

        # is_draw 역시 bool 속성이라고 가정
        self.assertTrue(board.is_draw)
        self.assertFalse(board.is_win)
        # 꽉 찼기 때문에 legal_moves는 빈 리스트여야 함
        self.assertEqual(board.legal_moves, [])

if __name__ == '__main__':
    unittest.main()


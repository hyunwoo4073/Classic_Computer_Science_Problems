# # connectfour_tests.py
# # Connect Four minimax tests based on Classic Computer Science Problems in Python
# import unittest
# from typing import List

# from minimax import find_best_move
# from connectfour import C4Board, C4Piece
# from board import Move


# def make_empty_board(turn: C4Piece = C4Piece.B) -> C4Board:
#     return C4Board(None, turn)


# class C4MinimaxTestCase(unittest.TestCase):
#     def test_vertical_win_in_one(self):
#         """
#         현재 차례가 B이고, 같은 컬럼에 B 세 개가 이미 쌓여 있을 때
#         같은 컬럼에 하나 더 두어서 바로 승리할 수 있는 상황을 만든다.
#         minimax가 그 컬럼을 선택하는지 확인.
#         """
#         columns: List[C4Board.Column] = [C4Board.Column() for _ in range(C4Board.NUM_COLUMNS)]

#         # 0번 컬럼에 B 세 개 쌓기 (row 0,1,2)
#         for _ in range(3):
#             columns[0].push(C4Piece.B)

#         board = C4Board(columns, turn=C4Piece.B)
#         best: Move = find_best_move(board)

#         # 0번 컬럼에 두면 세로 4개로 즉시 승리해야 한다.
#         self.assertEqual(best, 0)

#     def test_horizontal_win_in_one(self):
#         """
#         바닥(row 0)에 B, B, B 가 0~2번 컬럼에 깔려 있고
#         3번 컬럼이 비어있는 상황에서, B 차례일 때
#         3번 컬럼에 두어 가로로 4개를 완성하는지 확인.
#         """
#         columns: List[C4Board.Column] = [C4Board.Column() for _ in range(C4Board.NUM_COLUMNS)]

#         columns[0].push(C4Piece.B)
#         columns[1].push(C4Piece.B)
#         columns[2].push(C4Piece.B)
#         # columns[3]는 비워둠

#         board = C4Board(columns, turn=C4Piece.B)
#         best: Move = find_best_move(board)

#         self.assertEqual(best, 3)

#     def test_block_opponents_vertical_win(self):
#         """
#         상대(R)가 한 컬럼에 세 개를 쌓아둔 상태에서
#         내가(B) 한 수라도 안 막으면 다음 턴에 R이 바로 이기는 상황.
#         minimax가 해당 컬럼에 둬서 블로킹하는지 확인.
#         """
#         columns: List[C4Board.Column] = [C4Board.Column() for _ in range(C4Board.NUM_COLUMNS)]

#         # 2번 컬럼에 R 세 개 (row 0,1,2)
#         for _ in range(3):
#             columns[2].push(C4Piece.R)

#         # 다른 곳에는 약간 섞어둬도 상관 없음
#         columns[0].push(C4Piece.B)
#         columns[1].push(C4Piece.R)

#         # 지금은 B 차례, 안 막으면 R이 2번 컬럼으로 바로 승리
#         board = C4Board(columns, turn=C4Piece.B)
#         best: Move = find_best_move(board)

#         self.assertEqual(best, 2)

#     def test_legal_moves_respects_full_column(self):
#         """
#         맨 위까지 꽉 찬 컬럼은 legal_moves에 포함되지 않아야 한다.
#         minimax가 쓰기 위한 전제 조건으로도 중요하므로 같이 검증.
#         """
#         columns: List[C4Board.Column] = [C4Board.Column() for _ in range(C4Board.NUM_COLUMNS)]

#         # 1번 컬럼만 꽉 채운다.
#         for _ in range(C4Board.NUM_ROWS):
#             columns[1].push(C4Piece.B)

#         board = C4Board(columns, turn=C4Piece.B)
#         legal = board.legal_moves

#         # 1번 컬럼은 빠져 있어야 함
#         self.assertNotIn(1, legal)
#         # 나머지 컬럼은 포함되어야 함
#         expected = [c for c in range(C4Board.NUM_COLUMNS) if c != 1]
#         self.assertEqual(sorted(legal), expected)

#     def test_is_win_detects_four_in_a_row(self):
#         """
#         간단한 승리 상태를 만들어서 is_win이 True를 반환하는지 확인.
#         여기서는 세로 4개 B.
#         """
#         columns: List[C4Board.Column] = [C4Board.Column() for _ in range(C4Board.NUM_COLUMNS)]

#         for _ in range(4):
#             columns[4].push(C4Piece.B)

#         board = C4Board(columns, turn=C4Piece.R)

#         self.assertTrue(board.is_win)


# if __name__ == "__main__":
#     unittest.main()



# connectfour_tests.py
# 단위 테스트: Connect Four + minimax/alphabeta(find_best_move)

import unittest
from typing import List

from minimax import find_best_move
from connectfour import C4Board, C4Piece  # 네 파일 이름에 맞게 수정
from board import Move


def make_empty_columns() -> List[C4Board.Column]:
    return [C4Board.Column() for _ in range(C4Board.NUM_COLUMNS)]


class C4MinimaxTestCase(unittest.TestCase):
    def test_vertical_win_in_one(self):
        """
        B 차례에서 한 수면 세로 4개를 완성할 수 있는 상황:
        같은 컬럼에 B 3개 쌓여 있고, 위에 한 칸 비어 있음.
        find_best_move가 그 컬럼을 고르는지 확인.
        """
        cols = make_empty_columns()

        # 0번 컬럼에 B 3개 (row 0,1,2)
        for _ in range(3):
            cols[0].push(C4Piece.B)

        board = C4Board(cols, turn=C4Piece.B)
        best: Move = find_best_move(board, max_depth=3)

        self.assertEqual(best, 0)

    def test_horizontal_win_in_one(self):
        """
        바닥줄에 B, B, B 가 0~2번 컬럼에 있고,
        3번 컬럼이 비어있는 상태에서 B 차례.
        3번 컬럼을 골라 가로 4개로 승리하는지 확인.
        """
        cols = make_empty_columns()

        cols[0].push(C4Piece.B)
        cols[1].push(C4Piece.B)
        cols[2].push(C4Piece.B)
        # cols[3] 는 비움

        board = C4Board(cols, turn=C4Piece.B)
        best: Move = find_best_move(board, max_depth=3)

        self.assertEqual(best, 3)

    def test_block_opponents_vertical_win(self):
        """
        R가 2번 컬럼에 3개 쌓아둔 상태.
        지금 B 차례이고, 2번 컬럼을 막지 않으면
        다음 턴에 R가 바로 승리할 수 있는 상황.

        B가 2번 컬럼을 골라 블로킹하는지 확인.
        """
        cols = make_empty_columns()

        # 2번 컬럼: R 3개
        for _ in range(3):
            cols[2].push(C4Piece.R)

        # 다른 데는 약간 섞어 놓기 (큰 의미는 없음)
        cols[0].push(C4Piece.B)
        cols[1].push(C4Piece.R)

        board = C4Board(cols, turn=C4Piece.B)
        best: Move = find_best_move(board, max_depth=3)

        self.assertEqual(best, 2)

    def test_legal_moves_excludes_full_column(self):
        """
        한 컬럼이 꽉 찼을 때, 그 컬럼은 legal_moves에서 빠져 있어야 한다.
        minimax/alphabeta가 전제로 사용하는 기본 조건 체크.
        """
        cols = make_empty_columns()

        # 1번 컬럼만 꽉 채우기
        for _ in range(C4Board.NUM_ROWS):
            cols[1].push(C4Piece.B)

        board = C4Board(cols, turn=C4Piece.B)
        legal = board.legal_moves

        # 1번 컬럼은 포함되면 안 됨
        self.assertNotIn(1, legal)

        expected = [Move(c) for c in range(C4Board.NUM_COLUMNS) if c != 1]
        self.assertEqual(sorted(legal), sorted(expected))

    def test_is_win_detects_four_in_a_column(self):
        """
        단순한 승리 상태(세로 4개)를 만들어서
        is_win 속성이 True인지 확인.
        """
        cols = make_empty_columns()

        for _ in range(4):
            cols[4].push(C4Piece.B)

        board = C4Board(cols, turn=C4Piece.R)

        self.assertTrue(board.is_win)


if __name__ == "__main__":
    unittest.main()

# tictactoe_ai.py
from __future__ import annotations
from typing import Any
from board import Move
from tictactoe import TTTBoard
from play_ai import PlayAI


def tictactoe_move_parser(raw: str, board: TTTBoard) -> Move:
    """
    Tic-Tac-Toe에서는 0~8 인덱스를 받는다고 가정.
    예: "4" -> Move(4)
    필요하다면 "row col" -> Move(row * 3 + col) 같은 식으로 바꿔도 됨.
    """
    idx = int(raw)
    return Move(idx)


def main() -> None:
    board = TTTBoard()
    game = PlayAI(
        board=board,
        move_input_prompt="이동할 위치를 입력하세요 (0-8): ",
        move_parser=tictactoe_move_parser,
        depth=None,  # TTTBoard.AI_DEPTH 있으면 사용, 없으면 default (예: 8로 바꾸고 싶으면 depth=8)
    )
    game.run()


if __name__ == "__main__":
    main()

# connectfour_ai.py
from __future__ import annotations
from typing import Any
from board import Move
from connectfour import C4Board
from play_ai import PlayAI


def connectfour_move_parser(raw: str, board: C4Board) -> Move:
    """
    Connect Four에서는 입력을 '열 번호(int)'로만 받는다고 가정.
    예: "3" -> Move(3)
    """
    col = int(raw)
    return Move(col)


def main() -> None:
    board = C4Board()
    # C4Board에 AI_DEPTH가 있으면 자동으로 그걸 쓰고,
    # 없으면 PlayAI 내부 default 3을 사용.
    game = PlayAI(
        board=board,
        move_input_prompt="이동할 열 위치를 입력하세요 (0-6): ",
        move_parser=connectfour_move_parser,
        depth=None,  # 또는 명시적으로 depth=3
    )
    game.run()


if __name__ == "__main__":
    main()

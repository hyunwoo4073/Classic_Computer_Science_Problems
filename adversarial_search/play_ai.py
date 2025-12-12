# play_ai.py
from __future__ import annotations
from typing import Callable, Optional
from board import Board, Move
from minimax import find_best_move


class PlayAI:
    """
    사람 vs AI 게임 루프를 공통으로 처리하는 클래스.
    Board 인터페이스(legal_moves, move, is_win, is_draw, __repr__ 등)만 맞으면
    어떤 게임이든 재사용 가능.
    """

    def __init__(
        self,
        board: Board,
        move_input_prompt: str,
        move_parser: Callable[[str, Board], Move],
        depth: Optional[int] = None,
    ) -> None:
        """
        board           : 시작 보드 (예: C4Board(), TTTBoard())
        move_input_prompt : 사용자에게 보여줄 입력 프롬프트 문자열
        move_parser     : 입력 문자열과 현재 보드를 받아 Move 객체로 바꿔주는 함수
        depth           : minimax/alphabeta 탐색 깊이 (None이면 board.AI_DEPTH나 default 사용)
        """
        self.board = board
        self.move_input_prompt = move_input_prompt
        self.move_parser = move_parser

        if depth is None:
            # 보드에 AI_DEPTH가 정의되어 있으면 그걸 쓰고, 없으면 기본값 3
            depth = getattr(board, "AI_DEPTH", 3)
        self.depth = depth

    def get_player_move(self) -> Move:
        """사용자 입력을 받아 현재 보드에서 유효한 수(Move) 하나를 반환."""
        while True:
            try:
                raw = input(self.move_input_prompt)
                move = self.move_parser(raw, self.board)
            except Exception:
                print("입력을 다시 확인해주세요.")
                continue

            if move in self.board.legal_moves:
                return move
            else:
                print(f"해당 위치에는 둘 수 없습니다. 가능한 수: {self.board.legal_moves}")

    def run(self) -> None:
        """사람 vs AI 게임 루프를 실행."""
        print("게임을 시작합니다.")
        print(self.board)

        while True:
            # 1) 사람 수 두기
            human_move = self.get_player_move()
            self.board = self.board.move(human_move)
            print("\n당신의 수:")
            print(self.board)

            if self.board.is_win:
                print("당신이 이겼습니다!")
                break
            if self.board.is_draw:
                print("비겼습니다!")
                break

            # 2) AI 수 두기
            ai_move: Move = find_best_move(self.board, max_depth=self.depth)
            print(f"\nAI가 선택한 수: {ai_move}")
            self.board = self.board.move(ai_move)
            print(self.board)

            if self.board.is_win:
                print("AI가 이겼습니다!")
                break
            if self.board.is_draw:
                print("비겼습니다!")
                break

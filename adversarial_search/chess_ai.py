# # chess_ai.py
# # pip install python-chess 필요

# from __future__ import annotations
# from math import inf
# import chess

# # ─────────────────────────────
# # 평가 함수
# # ─────────────────────────────

# # 말 가치 (백 기준 점수)
# PIECE_VALUES = {
#     chess.PAWN:   100,
#     chess.KNIGHT: 320,
#     chess.BISHOP: 330,
#     chess.ROOK:   500,
#     chess.QUEEN:  900,
#     chess.KING:   0,   # 왕은 체크메이트로 따로 처리
# }

# def evaluate(board: chess.Board, original_player: bool) -> float:
#     """
#     original_player 입장에서의 점수 반환.
#     original_player: chess.WHITE 또는 chess.BLACK
#     """
#     # 게임 종료 상태 우선 처리
#     if board.is_checkmate():
#         # 현재 차례가 체크메이트 당한 것
#         # board.turn == 패배한 쪽
#         if board.turn == original_player:
#             return -10_000.0
#         else:
#             return 10_000.0

#     if board.is_stalemate() or board.is_insufficient_material():
#         return 0.0

#     # 말 가치 합산 (백 - 흑)
#     material = 0
#     for square, piece in board.piece_map().items():
#         value = PIECE_VALUES[piece.piece_type]
#         if piece.color == chess.WHITE:
#             material += value
#         else:
#             material -= value

#     # original_player 기준으로 부호 조정
#     if original_player == chess.WHITE:
#         return float(material)
#     else:
#         return float(-material)


# # ─────────────────────────────
# # alphabeta 탐색 (네가 준 시그니처)
# # ─────────────────────────────

# def alphabeta(
#     board: chess.Board,
#     maximizing: bool,
#     original_player: bool,
#     max_depth: int = 8,
#     alpha: float = float("-inf"),
#     beta: float = float("inf"),
# ) -> float:
#     """
#     board: python-chess의 chess.Board 객체
#     maximizing: 현재 노드가 original_player 입장에서 maximizing인지 여부
#     original_player: 탐색을 시작한 쪽 (chess.WHITE / chess.BLACK)
#     max_depth: 남은 탐색 깊이
#     alpha, beta: 알파-베타 경계값
#     """
#     # 기저 조건 - 종료 위치 또는 최대 깊이에 도달
#     if board.is_game_over() or max_depth == 0:
#         return evaluate(board, original_player)

#     # 재귀 조건 - 자신의 이익을 최대화하거나 상대방의 이익을 최소화
#     if maximizing:
#         for move in board.legal_moves:
#             board.push(move)
#             result = alphabeta(board, False, original_player, max_depth - 1, alpha, beta)
#             board.pop()
#             alpha = max(result, alpha)
#             if beta <= alpha:
#                 break  # 가지치기
#         return alpha
#     else:  # minimizing
#         for move in board.legal_moves:
#             board.push(move)
#             result = alphabeta(board, True, original_player, max_depth - 1, alpha, beta)
#             board.pop()
#             beta = min(result, beta)
#             if beta <= alpha:
#                 break  # 가지치기
#         return beta


# # ─────────────────────────────
# # 최선의 수 선택 함수
# # ─────────────────────────────

# def find_best_move(board: chess.Board, max_depth: int = 4) -> chess.Move:
#     """
#     현재 board.turn 쪽(다음에 둘 차례인 플레이어)을 original_player로 보고
#     alphabeta로 최선의 수 하나를 찾는다.
#     """
#     original_player = board.turn  # True=WHITE, False=BLACK

#     best_move: chess.Move | None = None
#     # original_player 입장에서 최대화
#     best_value = -inf

#     # 간단한 무브 오더링: 가운데 쪽 파일 우선 탐색 (체스판에서는 크게 중요하진 않지만 예제용)
#     legal_moves = list(board.legal_moves)

#     # 파일 중심 순서로 정렬 (e, d, f, c, g, b, h, a 느낌)
#     def move_file_score(m: chess.Move) -> int:
#         file = chess.square_file(m.to_square)  # 0~7 (a~h)
#         center = 3.5
#         return int(10 - abs(file - center))  # center에 가까울수록 점수 높게

#     legal_moves.sort(key=move_file_score, reverse=True)

#     for move in legal_moves:
#         board.push(move)
#         value = alphabeta(
#             board,
#             maximizing=False,          # 다음 깊이는 상대 입장
#             original_player=original_player,
#             max_depth=max_depth - 1,
#             alpha=float("-inf"),
#             beta=float("inf"),
#         )
#         board.pop()

#         if value > best_value or best_move is None:
#             best_value = value
#             best_move = move

#     # legal_moves가 비어있지 않다면 best_move는 None이 아니어야 함
#     if best_move is None:
#         raise RuntimeError("No legal moves available, but game is not over.")
#     return best_move


# # ─────────────────────────────
# # 콘솔용 간단 게임 루프
# # ─────────────────────────────

# def print_board(board: chess.Board) -> None:
#     print(board)
#     print("FEN:", board.fen())
#     print()

# def main():
#     board = chess.Board()
#     depth = 3  # 탐색 깊이 (3~4 정도에서 시작하는 걸 추천)

#     # 예시: 사람이 백, AI가 흑
#     human_color = chess.WHITE

#     while not board.is_game_over():
#         print_board(board)

#         if board.turn == human_color:
#             # 사람 차례
#             user_input = input("당신의 수를 입력하세요 (예: e2e4, q: 종료): ").strip()
#             if user_input.lower() == "q":
#                 print("게임을 종료합니다.")
#                 return
#             try:
#                 move = board.parse_uci(user_input)
#             except ValueError:
#                 print("잘못된 형식입니다. 다시 입력하세요.")
#                 continue

#             if move not in board.legal_moves:
#                 print("불법 수입니다. 다시 입력하세요.")
#                 continue

#             board.push(move)
#         else:
#             # AI 차례
#             print("AI가 생각 중입니다...")
#             ai_move = find_best_move(board, max_depth=depth)
#             print(f"AI 수: {ai_move.uci()}")
#             board.push(ai_move)

#     print_board(board)
#     print("게임 종료! 결과:", board.result())

# if __name__ == "__main__":
#     main()


# chess_gui_ai.py
# pip install python-chess 필요

from __future__ import annotations
from math import inf
import chess
import tkinter as tk
from typing import Optional

# ─────────────────────────────
# 평가 함수
# ─────────────────────────────

# 말 가치 (백 기준 점수)
PIECE_VALUES = {
    chess.PAWN:   100,
    chess.KNIGHT: 320,
    chess.BISHOP: 330,
    chess.ROOK:   500,
    chess.QUEEN:  900,
    chess.KING:   0,   # 왕은 체크메이트로 따로 처리
}

def evaluate(board: chess.Board, original_player: bool) -> float:
    """
    original_player 입장에서의 점수 반환.
    original_player: chess.WHITE 또는 chess.BLACK
    """
    # 게임 종료 상태 우선 처리
    if board.is_checkmate():
        # 현재 차례가 체크메이트 당한 것
        if board.turn == original_player:
            return -10_000.0
        else:
            return 10_000.0

    if board.is_stalemate() or board.is_insufficient_material():
        return 0.0

    # 말 가치 합산 (백 - 흑)
    material = 0
    for square, piece in board.piece_map().items():
        value = PIECE_VALUES[piece.piece_type]
        if piece.color == chess.WHITE:
            material += value
        else:
            material -= value

    # original_player 기준으로 부호 조정
    if original_player == chess.WHITE:
        return float(material)
    else:
        return float(-material)


# ─────────────────────────────
# alphabeta 탐색 (네가 준 시그니처 기반)
# ─────────────────────────────

def alphabeta(
    board: chess.Board,
    maximizing: bool,
    original_player: bool,
    max_depth: int = 3,
    alpha: float = float("-inf"),
    beta: float = float("inf"),
) -> float:
    """
    board: python-chess의 chess.Board 객체
    maximizing: 현재 노드가 original_player 입장에서 maximizing인지 여부
    original_player: 탐색을 시작한 쪽 (chess.WHITE / chess.BLACK)
    max_depth: 남은 탐색 깊이
    alpha, beta: 알파-베타 경계값
    """
    # 기저 조건 - 종료 위치 또는 최대 깊이에 도달
    if board.is_game_over() or max_depth == 0:
        return evaluate(board, original_player)

    # 재귀 조건 - 자신의 이익을 최대화하거나 상대방의 이익을 최소화
    if maximizing:
        for move in board.legal_moves:
            board.push(move)
            result = alphabeta(board, False, original_player, max_depth - 1, alpha, beta)
            board.pop()
            alpha = max(result, alpha)
            if beta <= alpha:
                break  # 가지치기
        return alpha
    else:  # minimizing
        for move in board.legal_moves:
            board.push(move)
            result = alphabeta(board, True, original_player, max_depth - 1, alpha, beta)
            board.pop()
            beta = min(result, beta)
            if beta <= alpha:
                break  # 가지치기
        return beta


# ─────────────────────────────
# 최선의 수 선택 함수
# ─────────────────────────────

def find_best_move(board: chess.Board, max_depth: int = 3) -> chess.Move:
    """
    현재 board.turn 쪽(다음에 둘 차례인 플레이어)을 original_player로 보고
    alphabeta로 최선의 수 하나를 찾는다.
    """
    original_player = board.turn  # True=WHITE, False=BLACK

    best_move: Optional[chess.Move] = None
    best_value = -inf  # original_player 입장에서 최대화

    # 간단한 무브 오더링: 중앙 파일 쪽을 우선
    legal_moves = list(board.legal_moves)

    def move_file_score(m: chess.Move) -> int:
        file_idx = chess.square_file(m.to_square)  # 0~7 (a~h)
        center = 3.5
        return int(10 - abs(file_idx - center))  # center에 가까울수록 점수 높게

    legal_moves.sort(key=move_file_score, reverse=True)

    for move in legal_moves:
        board.push(move)
        value = alphabeta(
            board,
            maximizing=False,          # 다음 깊이는 상대 입장
            original_player=original_player,
            max_depth=max_depth - 1,
            alpha=float("-inf"),
            beta=float("inf"),
        )
        board.pop()

        if value > best_value or best_move is None:
            best_value = value
            best_move = move

    if best_move is None:
        raise RuntimeError("No legal moves available, but game is not over.")
    return best_move


# ─────────────────────────────
# Tkinter 기반 GUI
# ─────────────────────────────

# 유니코드 말 표시
UNICODE_PIECES = {
    chess.Piece(chess.PAWN,   chess.WHITE): "♙",
    chess.Piece(chess.KNIGHT, chess.WHITE): "♘",
    chess.Piece(chess.BISHOP, chess.WHITE): "♗",
    chess.Piece(chess.ROOK,   chess.WHITE): "♖",
    chess.Piece(chess.QUEEN,  chess.WHITE): "♕",
    chess.Piece(chess.KING,   chess.WHITE): "♔",
    chess.Piece(chess.PAWN,   chess.BLACK): "♟",
    chess.Piece(chess.KNIGHT, chess.BLACK): "♞",
    chess.Piece(chess.BISHOP, chess.BLACK): "♝",
    chess.Piece(chess.ROOK,   chess.BLACK): "♜",
    chess.Piece(chess.QUEEN,  chess.BLACK): "♛",
    chess.Piece(chess.KING,   chess.BLACK): "♚",
}


class ChessGUI:
    def __init__(self, root: tk.Tk, depth: int = 3):
        self.root = root
        self.root.title("Chess AI (alphabeta + python-chess)")

        self.board = chess.Board()
        self.depth = depth

        self.square_size = 64
        self.board_size = self.square_size * 8

        self.canvas = tk.Canvas(
            root,
            width=self.board_size,
            height=self.board_size,
            bg="white",
            highlightthickness=0,
        )
        self.canvas.grid(row=0, column=0, columnspan=2)

        self.status_var = tk.StringVar()
        self.status_label = tk.Label(root, textvariable=self.status_var, font=("Arial", 12))
        self.status_label.grid(row=1, column=0, sticky="w")

        self.reset_button = tk.Button(root, text="새 게임", command=self.reset_game)
        self.reset_button.grid(row=1, column=1, sticky="e")

        # 사람은 White, AI는 Black으로 고정
        self.human_color = chess.WHITE

        self.selected_square: Optional[int] = None
        self.highlight_rect: Optional[int] = None

        self.canvas.bind("<Button-1>", self.on_click)

        self.draw_board()
        self.update_pieces()
        self.update_status()

    # ─── GUI 그리기 ───

    def draw_board(self):
        self.canvas.delete("square")
        colors = ("#EEEED2", "#769656")  # 라이트/다크 체스판 스타일 비슷하게
        for rank in range(8):
            for file in range(8):
                x1 = file * self.square_size
                y1 = (7 - rank) * self.square_size
                x2 = x1 + self.square_size
                y2 = y1 + self.square_size
                color = colors[(rank + file) % 2]
                self.canvas.create_rectangle(
                    x1, y1, x2, y2,
                    fill=color, tags=("square",),
                    outline=color,
                )

    def update_pieces(self):
        self.canvas.delete("piece")

        for square, piece in self.board.piece_map().items():
            file = chess.square_file(square)
            rank = chess.square_rank(square)

            x = file * self.square_size + self.square_size // 2
            y = (7 - rank) * self.square_size + self.square_size // 2

            symbol = UNICODE_PIECES.get(piece, "?")
            self.canvas.create_text(
                x, y,
                text=symbol,
                font=("Arial", int(self.square_size * 0.6)),
                tags=("piece",),
            )

    def highlight_square(self, square: Optional[int]):
        # 기존 하이라이트 제거
        if self.highlight_rect is not None:
            self.canvas.delete(self.highlight_rect)
            self.highlight_rect = None

        if square is None:
            return

        file = chess.square_file(square)
        rank = chess.square_rank(square)
        x1 = file * self.square_size
        y1 = (7 - rank) * self.square_size
        x2 = x1 + self.square_size
        y2 = y1 + self.square_size

        self.highlight_rect = self.canvas.create_rectangle(
            x1, y1, x2, y2,
            outline="yellow",
            width=3,
            tags=("highlight",),
        )

    # ─── 이벤트 및 로직 ───

    def reset_game(self):
        self.board.reset()
        self.selected_square = None
        self.highlight_square(None)
        self.draw_board()
        self.update_pieces()
        self.update_status()

    def on_click(self, event):
        if self.board.is_game_over():
            return

        # 사람 차례가 아니면 무시
        if self.board.turn != self.human_color:
            return

        file = event.x // self.square_size
        rank = 7 - (event.y // self.square_size)
        if file < 0 or file > 7 or rank < 0 or rank > 7:
            return

        clicked_square = chess.square(file, rank)

        # 선택이 안 된 상태에서
        if self.selected_square is None:
            piece = self.board.piece_at(clicked_square)
            # 자기 말만 선택 가능
            if piece is not None and piece.color == self.human_color:
                self.selected_square = clicked_square
                self.highlight_square(clicked_square)
            return
        else:
            # 이미 한 칸 선택한 뒤 → 두 번째 클릭
            from_sq = self.selected_square
            to_sq = clicked_square

            move = self.create_move(from_sq, to_sq)

            if move in self.board.legal_moves:
                self.board.push(move)
                self.selected_square = None
                self.highlight_square(None)
                self.update_pieces()
                self.update_status()

                if not self.board.is_game_over():
                    # 약간 딜레이 후 AI 수 두기
                    self.root.after(200, self.ai_move)
            else:
                # 같은 칸 다시 누르면 선택 해제
                if from_sq == to_sq:
                    self.selected_square = None
                    self.highlight_square(None)
                else:
                    # 다른 말 선택
                    piece = self.board.piece_at(clicked_square)
                    if piece is not None and piece.color == self.human_color:
                        self.selected_square = clicked_square
                        self.highlight_square(clicked_square)
                # 불법 수면 그냥 리턴
                return

    def create_move(self, from_sq: int, to_sq: int) -> chess.Move:
        """
        승진이 필요한 경우 자동으로 퀸 승진으로 처리.
        """
        move = chess.Move(from_sq, to_sq)

        # 승진이 필요한 경우, legal_moves 중에서 퀸 승진인 수를 찾아서 리턴
        if move not in self.board.legal_moves:
            # 승진 가능성 체크 (rank 도착이 끝 rank인지)
            piece = self.board.piece_at(from_sq)
            if piece is not None and piece.piece_type == chess.PAWN:
                dest_rank = chess.square_rank(to_sq)
                if dest_rank == 0 or dest_rank == 7:
                    promo_move = chess.Move(from_sq, to_sq, promotion=chess.QUEEN)
                    return promo_move

        return move

    def ai_move(self):
        if self.board.is_game_over():
            self.update_status()
            return

        if self.board.turn == self.human_color:
            return  # 뭔가 꼬인 경우 방지

        self.status_var.set("AI 생각 중...")
        self.root.update_idletasks()

        ai_move = find_best_move(self.board, max_depth=self.depth)
        self.board.push(ai_move)

        self.update_pieces()
        self.update_status()

    def update_status(self):
        if self.board.is_checkmate():
            if self.board.turn == self.human_color:
                self.status_var.set("체크메이트! AI 승리!")
            else:
                self.status_var.set("체크메이트! 당신의 승리!")
        elif self.board.is_stalemate():
            self.status_var.set("스테일메이트! 무승부.")
        elif self.board.is_insufficient_material():
            self.status_var.set("기물 부족. 무승부.")
        else:
            turn_str = "당신(백)" if self.board.turn == self.human_color else "AI(흑)"
            self.status_var.set(f"차례: {turn_str}")


# ─────────────────────────────
# main
# ─────────────────────────────

def main():
    root = tk.Tk()
    app = ChessGUI(root, depth=3)  # depth 조절 가능 (2~4 추천)
    root.mainloop()

if __name__ == "__main__":
    main()

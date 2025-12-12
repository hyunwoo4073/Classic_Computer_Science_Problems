from __future__ import annotations
from board import Piece, Board, Move

# 게임 플레이어의 가능한 최선의 움직임을 찾음
def minimax(board: Board, maximizing: bool, original_player: Piece, max_depth: int = 8) -> float:
    # 기저 조건 - 게임 종료 위치 또는 최대 깊이에 도달
    if board.is_win or board.is_draw or max_depth == 0:
        return board.evaluate(original_player)

    # 재귀 조건 - 이익을 극대화하거나 상대방의 이익을 최소화
    if maximizing:
        best_eval: float = float("-inf") # 낮은 시작 점수
        for move in board.legal_moves:
            result: float = minimax(board.move(move), False, original_player, max_depth - 1)
            best_eval = max(result, best_eval) # 가장 높은 평가를 받은 위치로 움직임
        return best_eval
    else: # 최소화
        worst_eval: float = float("inf") # 높은 시작 점수
        for move in board.legal_moves:
            result = minimax(board.move(move), True, original_player, max_depth - 1)
            worst_eval = min(result, worst_eval) # 가장 낮은 평가를 받은 위치로 움직임
        return worst_eval

def alphabeta(board: Board, maximizing: bool, original_player: Piece, max_depth: int = 8, alpha: float = float("-inf"), beta: float = float("inf")) -> float:
    # 기저 조건 - 종료 위치 또는 최대 깊이에 도달
    if board.is_win or board.is_draw or max_depth == 0:
        return board.evaluate(original_player)

    # 재귀 조건 - 자신의 이익을 최대화하거나 상대방의 이익을 최소화
    if maximizing:
        for move in board.legal_moves:
            result: float = alphabeta(board.move(move), False, original_player, max_depth - 1, alpha, beta)
            alpha = max(result, alpha)
            if beta <= alpha:
                break
        return alpha
    else:  # minimizing
        for move in board.legal_moves:
            result = alphabeta(board.move(move), True, original_player, max_depth - 1, alpha, beta)
            beta = min(result, beta)
            if beta <= alpha:
                break
        return beta

# 최대 깊이(max_depth) 전까지 최선의 움직임을 찾음
def find_best_move(board: Board, max_depth: int = 8) -> Move:
    best_eval: float = float("-inf")
    best_move: Move = Move(-1)
    for move in board.legal_moves:
        result: float = alphabeta(board.move(move), False, board.turn, max_depth)
        if result > best_eval:
            best_eval = result
            best_move = move
    return best_move

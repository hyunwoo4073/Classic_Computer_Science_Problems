# connectfour_ai.py
from __future__ import annotations
from minimax import find_best_move
from connectfour import C4Board
from board import Move, Board


board: Board = C4Board()


def get_player_move() -> Move:
    while True:
        try:
            col = int(input("당신의 수를 입력하세요 (0~6): "))
            mv = Move(col)
            if mv in board.legal_moves:
                return mv
            print("해당 열에는 둘 수 없습니다.")
        except ValueError:
            print("숫자를 입력해주세요.")


# --------------------------------------------
# 사람 vs AI
# --------------------------------------------
def play_human_vs_ai(depth=3):
    global board
    board = C4Board()

    while True:
        human = get_player_move()
        board = board.move(human)

        if board.is_win:
            print("당신이 이겼습니다!")
            break
        if board.is_draw:
            print("무승부입니다!")
            break

        ai = find_best_move(board, depth)
        print(f"AI가 {ai} 열을 선택했습니다.")
        board = board.move(ai)
        print(board)

        if board.is_win:
            print("AI 승리!")
            break
        if board.is_draw:
            print("무승부입니다!")
            break


# --------------------------------------------
# AI vs AI (한 판)
# --------------------------------------------
def play_ai_vs_ai_single(depth=3, verbose=False) -> int:
    board: Board = C4Board()
    current = 1  # 1P = 선공(B), 2P = 후공(R)

    while True:
        move = find_best_move(board, depth)
        board = board.move(move)
        if verbose:
            print(f"[플레이어 {current}] {move} 수:")
            print(board)

        if board.is_win:
            return current
        if board.is_draw:
            return 0

        current = 2 if current == 1 else 1


# --------------------------------------------
# AI vs AI 여러 판 시뮬레이션
# --------------------------------------------
def simulate_ai_vs_ai(games=20, depth=3):
    first = second = draw = 0

    for _ in range(games):
        result = play_ai_vs_ai_single(depth, verbose=False)
        if result == 1:
            first += 1
        elif result == 2:
            second += 1
        else:
            draw += 1

    print("\n=== 시뮬레이션 결과 ===")
    print(f"총 {games}판")
    print(f"선공 승리 : {first}")
    print(f"후공 승리 : {second}")
    print(f"무승부    : {draw}")


if __name__ == "__main__":
    mode = input("1: 사람 vs AI, 2: AI vs AI 시뮬레이션 → ")
    if mode == "1":
        play_human_vs_ai(depth=3)
    else:
        simulate_ai_vs_ai(games=20, depth=3)

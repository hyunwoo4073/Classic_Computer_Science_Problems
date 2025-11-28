# from typing import NamedTuple, List, Dict, Optional
# import random
# from csp import CSP, Constraint   # 네가 만든 csp.py 기준


# # -----------------------
# # 스도쿠용 기본 타입 정의
# # -----------------------

# class Cell(NamedTuple):
#     row: int   # 0 ~ 8
#     col: int   # 0 ~ 8


# # -----------------------
# # 스도쿠 제약 조건 클래스
# # -----------------------

# class SudokuConstraint(Constraint[Cell, int]):
#     """
#     - 같은 행(row) 안에서는 숫자 중복 X
#     - 같은 열(col) 안에서는 숫자 중복 X
#     - 같은 3x3 박스 안에서는 숫자 중복 X
#     """
#     def __init__(self, cells: List[Cell]) -> None:
#         super().__init__(cells)
#         size = 9

#         # 행/열/박스 유닛 미리 구성
#         self.rows: List[List[Cell]] = [
#             [Cell(r, c) for c in range(size)] for r in range(size)
#         ]
#         self.cols: List[List[Cell]] = [
#             [Cell(r, c) for r in range(size)] for c in range(size)
#         ]
#         self.boxes: List[List[Cell]] = []
#         for br in range(0, size, 3):
#             for bc in range(0, size, 3):
#                 box = [
#                     Cell(r, c)
#                     for r in range(br, br + 3)
#                     for c in range(bc, bc + 3)
#                 ]
#                 self.boxes.append(box)

#     def satisfied(self, assignment: Dict[Cell, int]) -> bool:
#         # 각 유닛(행/열/박스) 안의 값 중복 체크
#         for unit in self.rows + self.cols + self.boxes:
#             seen: set[int] = set()
#             for cell in unit:
#                 if cell in assignment:
#                     v = assignment[cell]
#                     if v in seen:
#                         return False
#                     seen.add(v)
#         return True


# # -----------------------
# # 공통 유틸: 그리드 출력
# # -----------------------

# def print_grid(grid: List[List[int]]) -> None:
#     for r in range(9):
#         print(" ".join(str(v) if v != 0 else "." for v in grid))


# # -----------------------
# # CSP 객체 만들기 helper
# # -----------------------

# def build_sudoku_csp(grid: List[List[int]]) -> CSP[Cell, int]:
#     """
#     0은 빈칸, 1~9는 이미 채워진 값인 9x9 grid를 받아
#     SudokuConstraint가 설정된 CSP 객체를 만들어준다.
#     """
#     size = 9
#     variables: List[Cell] = [Cell(r, c) for r in range(size) for c in range(size)]

#     domains: Dict[Cell, List[int]] = {}
#     for r in range(size):
#         for c in range(size):
#             cell = Cell(r, c)
#             if grid[r][c] == 0:
#                 # 빈칸이면 1~9 가능
#                 domain = list(range(1, 10))
#                 random.shuffle(domain)  # 약간의 랜덤성 부여 (생성 시 다양성 ↑)
#                 domains[cell] = domain
#             else:
#                 # 이미 숫자가 있으면 그 숫자만 허용
#                 domains[cell] = [grid[r][c]]

#     csp: CSP[Cell, int] = CSP(variables, domains)
#     csp.add_constraint(SudokuConstraint(variables))
#     return csp


# # -----------------------
# # 1) 스도쿠 풀이 함수
# # -----------------------

# def solve_sudoku(grid: List[List[int]]) -> Optional[List[List[int]]]:
#     """
#     grid: 9x9, 0은 빈칸, 1~9는 채워진 숫자
#     반환: 해가 있으면 채워진 9x9 grid, 없으면 None
#     """
#     csp = build_sudoku_csp(grid)
#     solution = csp.backtracking_search()
#     if solution is None:
#         return None

#     size = 9
#     solved: List[List[int]] = [[0 for _ in range(size)] for _ in range(size)]
#     for cell, val in solution.items():
#         solved[cell.row][cell.col] = val
#     return solved


# # -----------------------
# # 2) 해 개수 세기 (유일해 검증용)
# # -----------------------

# def _count_solutions(csp: CSP[Cell, int],
#                      assignment: Optional[Dict[Cell, int]] = None,
#                      limit: int = 2) -> int:
#     """
#     주어진 CSP에 대해 해의 개수를 센다.
#     - limit 개 이상 발견되면 바로 종료 (유일성 검사용)
#     """
#     if assignment is None:
#         assignment = {}

#     if len(assignment) == len(csp.variables):
#         return 1  # 한 개 해 발견

#     # 아직 할당 안 된 변수 하나 선택
#     unassigned: List[Cell] = [v for v in csp.variables if v not in assignment]
#     first: Cell = unassigned[0]

#     total = 0
#     for value in csp.domains[first]:
#         local = assignment.copy()
#         local[first] = value
#         if csp.consistent(first, local):
#             total += _count_solutions(csp, local, limit)
#             if total >= limit:
#                 break
#     return total


# def has_unique_solution(grid: List[List[int]]) -> bool:
#     """
#     현재 grid가 해를 딱 1개만 가지는지 확인.
#     (2개 이상이면 False)
#     """
#     csp = build_sudoku_csp(grid)
#     cnt = _count_solutions(csp, limit=2)
#     return cnt == 1


# # -----------------------
# # 3) 완성된 해(전체 채워진 스도쿠) 생성
# # -----------------------

# def generate_full_solution() -> List[List[int]]:
#     """
#     아무 숫자도 없는 빈 퍼즐에서
#     랜덤한 완성 스도쿠 해 하나를 생성.
#     """
#     empty = [[0 for _ in range(9)] for _ in range(9)]
#     solved = solve_sudoku(empty)
#     if solved is None:
#         raise RuntimeError("스도쿠 해를 생성하지 못했습니다.")
#     return solved


# # -----------------------
# # 4) 퍼즐 자동 생성
# # -----------------------

# def generate_sudoku_puzzle(clues: int = 30) -> List[List[int]]:
#     """
#     완성된 스도쿠 해를 먼저 만든 뒤,
#     숫자를 지워 나가면서 '유일 해'를 유지하는 퍼즐을 생성.
#     clues: 남겨둘 숫자 개수 (대략적인 힌트 개수)
#     """
#     full = generate_full_solution()
#     puzzle = [row[:] for row in full]  # 깊은 복사

#     # 모든 셀 좌표를 섞는다
#     cells: List[Cell] = [Cell(r, c) for r in range(9) for c in range(9)]
#     random.shuffle(cells)

#     # 현재 남은 힌트 개수
#     def count_clues(g: List[List[int]]) -> int:
#         return sum(1 for r in range(9) for c in range(9) if g[r][c] != 0)

#     for cell in cells:
#         if count_clues(puzzle) <= clues:
#             break  # 더 이상 안 지우고 종료

#         r, c = cell.row, cell.col
#         backup = puzzle[r][c]
#         if backup == 0:
#             continue

#         puzzle[r][c] = 0
#         # 지운 뒤에도 해가 유일한지 검사
#         if not has_unique_solution(puzzle):
#             # 유일하지 않으면 다시 복구
#             puzzle[r][c] = backup

#     return puzzle


# # -----------------------
# # 테스트 실행
# # -----------------------

# if __name__ == "__main__":
#     # 1) 퍼즐 자동 생성
#     puzzle = generate_sudoku_puzzle(clues=30)
#     print("=== 생성된 퍼즐 ===")
#     print_grid(puzzle)
#     print()

#     # 2) 퍼즐 풀이
#     solved = solve_sudoku(puzzle)
#     if solved is None:
#         print("해를 찾지 못했습니다.")
#     else:
#         print("=== 풀이 결과 ===")
#         print_grid(solved)
from typing import NamedTuple, List, Dict, Optional
from csp import CSP, Constraint  # 네가 만든 CSP/Constraint 모듈

# 스도쿠 셀을 나타내는 좌표
class Cell(NamedTuple):
    row: int  # 0 ~ 8
    col: int  # 0 ~ 8

# 스도쿠 제약조건: 같은 행/열/3x3 박스 안에 중복 숫자 X
class SudokuConstraint(Constraint[Cell, int]):
    def __init__(self, cells: List[Cell]) -> None:
        super().__init__(cells)
        self.cells = cells
        size = 9

        # 각 행, 열, 박스 유닛을 미리 만들어 둔다.
        self.rows: List[List[Cell]] = [
            [Cell(r, c) for c in range(size)] for r in range(size)
        ]
        self.cols: List[List[Cell]] = [
            [Cell(r, c) for r in range(size)] for c in range(size)
        ]
        self.boxes: List[List[Cell]] = []
        for br in range(0, size, 3):
            for bc in range(0, size, 3):
                box = [
                    Cell(r, c)
                    for r in range(br, br + 3)
                    for c in range(bc, bc + 3)
                ]
                self.boxes.append(box)

    def satisfied(self, assignment: Dict[Cell, int]) -> bool:
        # 각 유닛(행/열/박스)마다 값 중복이 있는지 확인
        for unit in self.rows + self.cols + self.boxes:
            seen: set[int] = set()
            for cell in unit:
                if cell in assignment:
                    v = assignment[cell]
                    if v in seen:
                        return False
                    seen.add(v)
        return True


def solve_sudoku(grid: List[List[int]]) -> Optional[List[List[int]]]:
    """
    grid: 9x9, 0은 빈칸, 1~9는 채워진 숫자
    반환: 해가 있으면 채워진 9x9 grid, 없으면 None
    """
    size = 9
    variables: List[Cell] = [Cell(r, c) for r in range(size) for c in range(size)]

    # 도메인 설정: 채워진 칸은 {해당 숫자}, 빈칸은 {1..9}
    domains: Dict[Cell, List[int]] = {}
    for r in range(size):
        for c in range(size):
            cell = Cell(r, c)
            if grid[r][c] == 0:
                domains[cell] = list(range(1, 10))
            else:
                domains[cell] = [grid[r][c]]

    csp: CSP[Cell, int] = CSP(variables, domains)
    csp.add_constraint(SudokuConstraint(variables))

    solution = csp.backtracking_search()
    if solution is None:
        return None

    solved: List[List[int]] = [[0 for _ in range(size)] for _ in range(size)]
    for cell, val in solution.items():
        solved[cell.row][cell.col] = val
    return solved


# (선택) 출력용 헬퍼
def print_grid(grid: List[List[int]]) -> None:
    for r in range(9):
        print(" ".join(str(v) if v != 0 else "." for v in grid))


if __name__ == "__main__":
    # 예시 퍼즐 (0 = 빈칸)
    puzzle: List[List[int]] = [
        [0, 0, 0, 2, 6, 0, 7, 0, 1],
        [6, 8, 0, 0, 7, 0, 0, 9, 0],
        [1, 9, 0, 0, 0, 4, 5, 0, 0],
        [8, 2, 0, 1, 0, 0, 0, 4, 0],
        [0, 0, 4, 6, 0, 2, 9, 0, 0],
        [0, 5, 0, 0, 0, 3, 0, 2, 8],
        [0, 0, 9, 3, 0, 0, 0, 7, 4],
        [0, 4, 0, 0, 5, 0, 0, 3, 6],
        [7, 0, 3, 0, 1, 8, 0, 0, 0],
    ]

    print("=== 입력 ===")
    print_grid(puzzle)
    print()

    solved = solve_sudoku(puzzle)
    if solved is None:
        print("해 없음")
    else:
        print("=== 해 ===")
        print_grid(solved)

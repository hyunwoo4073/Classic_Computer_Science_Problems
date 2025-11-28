#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from __future__ import annotations
from typing import NamedTuple, List, Dict, Optional
from csp import CSP, Constraint  # 네가 이미 가지고 있는 csp 모듈

# 타입 정의 --------------------------------------------------------------------

# 보드를 단순히 2차원 문자 격자로 표현 ('.' = 빈칸, 글자 = 부품 ID)
Board = List[List[str]]

class Cell(NamedTuple):
    row: int
    col: int

ComponentId = str          # "U1", "R1", "C5" 같은 부품 이름
Placement   = List[Cell]   # 해당 부품이 차지하는 모든 셀 좌표 리스트


# 유틸 함수 --------------------------------------------------------------------

def create_board(rows: int, cols: int) -> Board:
    """rows x cols 크기의 빈 보드 생성."""
    return [["." for _ in range(cols)] for _ in range(rows)]


def display_board(board: Board) -> None:
    """보드 출력."""
    for row in board:
        print("".join(row))


# 도메인 생성 -------------------------------------------------------------------

def generate_component_domain(
    height: int,
    width: int,
    board_rows: int,
    board_cols: int,
) -> List[Placement]:
    """
    특정 부품(높이 x 너비)이 보드 위에 놓일 수 있는 모든 위치 후보(Placement 리스트)를 생성.
    단순하게 회전은 고려하지 않고, (row, col)이 부품의 왼쪽 위라고 가정.
    """
    domain: List[Placement] = []

    # 부품의 왼쪽 위가 될 수 있는 모든 (row, col)를 순회
    for row in range(board_rows - height + 1):
        for col in range(board_cols - width + 1):
            cells: Placement = []
            for dr in range(height):
                for dc in range(width):
                    cells.append(Cell(row + dr, col + dc))
            domain.append(cells)

    return domain


# 제약 조건 ---------------------------------------------------------------------

class LayoutConstraint(Constraint[ComponentId, Placement]):
    """
    회로판 레이아웃 제약:
    - 서로 다른 부품의 footprint(Placement)가 같은 셀을 공유하면 안 된다.
    - margin > 0 으로 설정하면, 해당 부품 주변 margin 칸까지도 서로 겹치지 않게 할 수 있음.
      (간단한 부품 간 최소 간격 제약)
    """

    def __init__(self, components: List[ComponentId], margin: int = 0) -> None:
        super().__init__(components)
        self.components = components
        self.margin = margin

    def _expanded_cells(self, placement: Placement) -> List[Cell]:
        """
        margin 이 0이면 placement 그대로,
        margin 이 1 이상이면 각 셀 주변까지 확장된 '금지 영역'을 리턴.
        """
        if self.margin <= 0:
            return placement

        expanded: List[Cell] = []
        seen: set[Cell] = set()

        for cell in placement:
            for dr in range(-self.margin, self.margin + 1):
                for dc in range(-self.margin, self.margin + 1):
                    nr = cell.row + dr
                    nc = cell.col + dc
                    c = Cell(nr, nc)
                    if c not in seen:
                        seen.add(c)
                        expanded.append(c)
        return expanded

    def satisfied(self, assignment: Dict[ComponentId, Placement]) -> bool:
        used: set[Cell] = set()

        for comp, placement in assignment.items():
            # 이 부품이 차지하는 셀(또는 margin 포함 금지 영역)
            cells = self._expanded_cells(placement)

            for cell in cells:
                # 보드 밖 좌표는 도메인 생성에서 이미 걸러졌다고 가정하므로 여기선 체크 안 함
                if cell in used:
                    # 이미 다른 부품이 이 영역을 사용 중 → 겹침 발생 → 실패
                    return False
                used.add(cell)

        return True


# 메인 -------------------------------------------------------------------------

if __name__ == "__main__":
    # 보드 크기 (예: 10 x 20)
    BOARD_ROWS = 9
    BOARD_COLS = 9

    board: Board = create_board(BOARD_ROWS, BOARD_COLS)

    # 부품 정의: {부품ID: (height, width)}
    # height = 세로 셀 개수, width = 가로 셀 개수
    components_spec: Dict[ComponentId, tuple[int, int]] = {
        "U1": (4, 4),  # 3x4 크기
        "T2": (3, 3),  # 2x5 크기
        "X1": (1, 6),  # 1x3 크기
        "Y2": (2, 5),
        "C1": (2, 2),
    }

    # CSP 도메인 구성: 각 부품 → 가능한 Placement 리스트
    domains: Dict[ComponentId, List[Placement]] = {}
    for cid, (h, w) in components_spec.items():
        domains[cid] = generate_component_domain(
            height=h,
            width=w,
            board_rows=BOARD_ROWS,
            board_cols=BOARD_COLS,
        )

    # CSP 생성
    variables: List[ComponentId] = list(components_spec.keys())
    csp: CSP[ComponentId, Placement] = CSP(variables, domains)

    # 레이아웃 제약 추가 (margin=0 → footprint끼리만 안 겹치면 됨)
    # margin을 1 이상으로 주면 부품 사이에 최소 1셀 간격 유지
    csp.add_constraint(LayoutConstraint(variables, margin=0))

    # 해 탐색
    solution: Optional[Dict[ComponentId, Placement]] = csp.backtracking_search()

    if solution is None:
        print("배치 해를 찾을 수 없습니다.")
    else:
        # 찾은 해를 보드에 반영
        for cid, placement in solution.items():
            for cell in placement:
                # 같은 칸에 여러 글자를 쓰지 않도록 보드가 비어 있을 때만 찍도록 방어
                if board[cell.row][cell.col] == ".":
                    # 부품 이름 첫 글자로 표시
                    board[cell.row][cell.col] = cid[0]

        print("=== 배치 결과 보드 ===")
        display_board(board)

        print("\n=== 각 부품의 배치 좌표 ===")
        for cid, placement in solution.items():
            print(f"{cid}: {placement}")

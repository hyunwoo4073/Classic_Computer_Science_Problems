from enum import Enum
from typing import List, NamedTuple, Callable, Optional
import random
from math import sqrt
from generic_search import dfs, bfs, node_to_path, astar, Node
# from generic_search import dfs, Node, node_to_path, bfs

class Cell(str, Enum):
    EMPTY = " "
    BLOCKED = "X"
    START = "S"
    GOAL = "G"
    PATH = "*"

class MazeLocation(NamedTuple):
    row: int
    column: int

class Maze:
    def __init__(self, rows: int = 10, columns: int = 10,
                 sparseness: float = 0.2,
                 start: MazeLocation = MazeLocation(0, 0),
                 goal: MazeLocation = MazeLocation(9, 9)) -> None:
        # 기본 인스턴스 변수 초기화
        self._rows: int = rows
        self._columns: int = columns
        self.start: MazeLocation = start
        self.goal: MazeLocation = goal
        # 격자를 빈 공간으로 채움
        self._grid: List[List[Cell]] = [[Cell.EMPTY for c in range(columns)] for r in range(rows)]
        # 격자에 막힌 공간을 무작위로 채움
        self._randomly_fill(rows, columns, sparseness)
        # 시작 위치와 목표 위치를 설정
        self._grid[start.row][start.column] = Cell.START
        self._grid[goal.row][goal.column] = Cell.GOAL

    def _randomly_fill(self, rows: int, columns: int, sparseness: float):
        for row in range(rows):
            for column in range(columns):
                if random.uniform(0, 1.0) < sparseness:
                    self._grid[row][column] = Cell.BLOCKED

    def __str__(self) -> str:
        output: str = ""
        for row in self._grid:
            output += "".join([c.value for c in row]) + "\n"
        return output

    def goal_test(self, ml: MazeLocation) -> bool:
        return ml == self.goal

    def successors(self, ml: MazeLocation) -> List[MazeLocation]:
        locations: List[MazeLocation] = []
        if ml.row +1 < self._rows and self._grid[ml.row + 1][ml.column] != Cell.BLOCKED:
            locations.append(MazeLocation(ml.row + 1, ml.column))
        if ml.row - 1 >= 0 and self._grid[ml.row - 1][ml.column] != Cell.BLOCKED:
            locations.append(MazeLocation(ml.row - 1, ml.column))
        if ml.column + 1 < self._columns and self._grid[ml.row][ml.column + 1] != Cell.BLOCKED:
            locations.append(MazeLocation(ml.row, ml.column + 1))
        if ml.column - 1 >=0 and self._grid[ml.row][ml.column - 1] != Cell.BLOCKED:
            locations.append(MazeLocation(ml.row, ml.column - 1))
        return locations

    def mark(self, path: List[MazeLocation]):
        for maze_location in path:
            self._grid[maze_location.row][maze_location.column] = Cell.PATH
        self._grid[self.start.row][self.start.column] = Cell.START
        self._grid[self.goal.row][self.goal.column] = Cell.GOAL

    def clear(self, path: List[MazeLocation]):
        for maze_location in path:
            self._grid[maze_location.row][maze_location.column] = Cell.EMPTY
        self._grid[self.start.row][self.start.column] = Cell.START
        self._grid[self.goal.row][self.goal.column] = Cell.GOAL

def euclidean_distance(goal: MazeLocation) -> Callable[[MazeLocation], float]:
    def distance(ml: MazeLocation) -> float:
        xdist: int = ml.column - goal.column
        ydist: int = ml.row - goal.row
        return sqrt((xdist * xdist) + (ydist * ydist))
    return distance

def manhattan_distance(goal: MazeLocation) -> Callable[[MazeLocation], float]:
    def distance(ml: MazeLocation) -> float:
        xdist: int = abs(ml.column - goal.column)
        ydist: int = abs(ml.row - goal.row)
        return (xdist + ydist)
    return distance

# maze: Maze = Maze()
# print(maze)

if __name__ == "__main__":
    # 깊이 우선 탐색(DFS)
    m: Maze = Maze()
    print(m)
    solution1: Optional[Node[MazeLocation]] = dfs(m.start, m.goal_test, m.successors)
    if solution1 is None:
        print("깊이 우선 탐색으로 길을 찾을 수 없습니다!")
    else:
        path1: List[MazeLocation] = node_to_path(solution1)
        m.mark(path1)
        print("깊이 우선 탐색\n")
        print(m)
        m.clear(path1)

    # 너비 우선 탐색(BFS)
    solution2: Optional[Node[MazeLocation]] = bfs(m.start, m.goal_test, m.successors)
    if solution2 is None:
        print("너비 우선 탐색으로 길을 찾을 수 없습니다!")
    else:
        path2: List[MazeLocation] = node_to_path(solution2)
        m.mark(path2)
        print("너비 우선 탐색\n")
        print(m)
        m.clear(path2)

    # Test A*
    distance: Callable[[MazeLocation], float] = manhattan_distance(m.goal)
    solution3: Optional[Node[MazeLocation]] = astar(m.start, m.goal_test, m.successors, distance)
    if solution3 is None:
        print("A* 알고리즘으로 길을 찾을 수 없습니다!")
    else:
        path3: List[MazeLocation] = node_to_path(solution3)
        m.mark(path3)
        print("A*\n")
        print(m)
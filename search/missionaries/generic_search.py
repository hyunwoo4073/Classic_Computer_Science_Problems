from __future__ import annotations
from typing import TypeVar, Iterable, Sequence, Generic, List, Callable, Set, Deque, Dict, Any, Optional, Protocol
from heapq import heappush, heappop

T = TypeVar('T')

def linear_contains(iterable: Iterable[T], key: T) -> bool:
    for item in iterable:
        if item == key:
            return True
    return False

C = TypeVar("C", bound="Comparable")

class Comparable(Protocol):
    def __eq__(self, other: Any) -> bool:
        ...
    def __lt__(self: C, other: C) -> bool:
        ...
    def __gt__(self: C, other: C) -> bool:
        return (not self < other) and self != other
    def __le__(self: C, other: C) -> bool:
        return self < other or self == other

    def __ge__(self: C, other: C) -> bool:
        return not self < other

def binary_contains(Sequence: Sequence[C], key: C) -> bool:
    low: int = 0
    high: int = len(Sequence) - 1
    while low <= high:
        mid: int = (low + high) // 2
        if Sequence[mid] < key:
            low = mid + 1
        elif Sequence[mid] > key:
            high = mid - 1
        else:
            return True
    return False

class Stack(Generic[T]):
    def __init__(self) -> None:
        self._container: List[T] = []
    
    @property
    def empty(self) -> bool:
        return not self._container # 컨테이너가 비었다면 false가 아님(=true)
    
    def push(self, item: T) -> None:
        self._container.append(item)
    
    def pop(self) -> T:
        return self._container.pop()

    def __repr__(self) -> str:
        return repr(self._container)

class Node(Generic[T]):
    def __init__(self, state: T, parent: Optional[Node], cost: float = 0.0, heuristic: float = 0.0) -> None:
        self.state: T = state
        self.parent: Optional[Node] = parent
        self.cost: float = cost
        self.heuristic: float = heuristic

    def __lt__(self, other: Node) -> bool:
        return(self.cost + self.heuristic) < (other.cost + other.heuristic)

# def dfs(initial: T, goal_test: Callable[[T], bool], successors: Callable[[T], List[T]]) -> Optional[Node[T]]:
#     # frontier는 아직 방문하지 않은 곳
#     frontier: Stack[Node[T]] = Stack()
#     frontier.push(Node(initial, None))
#     # explored는 이미 방문한 곳
#     explored: Set[T] = {initial}

#     # 방문할 곳이 더 있는지 탐색
#     while not frontier.empty:
#         current_node: Node[T] = frontier.pop()
#         current_state: T = current_node.state
#         # 목표 지점을 찾았다면 종료
#         if goal_test(current_state):
#             return current_node
#         # 방문하지 않은 다음 장소가 있는지 확인
#         for child in successors(current_state):
#             if child in explored: # 이미 방문한 자식 노드(장소)라면 건너뜀
#                 continue
#             explored.add(child)
#             frontier.push(Node(child, current_node))
#     return None # 모든 곳을 방문했지만 결국 목표 지점을 찾지 못함

# counter 추가
def dfs(initial: T,
        goal_test: Callable[[T], bool],
        successors: Callable[[T], List[T]]) -> Tuple[Optional[Node[T]], int]:
    # frontier는 아직 방문하지 않은 곳
    frontier: Stack[Node[T]] = Stack()
    frontier.push(Node(initial, None))
    # explored는 이미 방문한 곳
    explored: Set[T] = {initial}

    visited_count: int = 0  # 🔹 탐색한 지점 수

    # 방문할 곳이 더 있는지 탐색
    while not frontier.empty:
        current_node: Node[T] = frontier.pop()
        visited_count += 1  # 🔹 지금 팝한 노드를 방문했다고 카운트
        current_state: T = current_node.state
        # 목표 지점을 찾았다면 종료
        if goal_test(current_state):
            return current_node, visited_count
        # 방문하지 않은 다음 장소가 있는지 확인
        for child in successors(current_state):
            if child in explored:
                continue
            explored.add(child)
            frontier.push(Node(child, current_node))
    return None, visited_count 

def node_to_path(node: Node[T]) -> List[T]:
    path: List[T] = [node.state]
    # 노드 경로를 반전
    while node.parent is not None:
        node = node.parent
        path.append(node.state)
    path.reverse()
    return path

class Queue(Generic[T]):
    def __init__(self) -> None:
        self._container: Deque[T] = Deque()
    
    @property
    def empty(self) -> bool:
        return not self._container # 컨테이너가 비었다면 false가 아님(=true)

    def push(self, item: T) -> None:
        self._container.append(item)

    def pop(self) -> T:
        return self._container.popleft() # 선입선출(FIFO)

    def __repr__(self) -> str:
        return repr(self._container)

# def bfs(initial: T, goal_test: Callable[[T], bool], successors: Callable[[T], List[T]]) -> Optional[Node[T]]:
#     # frontier는 아직 방문하지 않은 곳
#     frontier: Queue[Node[T]] = Queue()
#     frontier.push(Node(initial, None))
#     # explored는 이미 방문한 곳
#     explored: Set[T] = {initial}

#     # 방문할 곳이 더 있는지 탐색
#     while not frontier.empty:
#         current_node: Node[T] = frontier.pop()
#         current_state: T = current_node.state
#         # 목표 지점을 찾았다면 종료
#         if goal_test(current_state):
#             return current_node
#         # 방문하지 않은 다음 장소가 있는지 확인
#         for child in successors(current_state):
#             if child in explored:
#                 continue
#             explored.add(child)
#             frontier.push(Node(child, current_node))
#     return None

# counter 추가
def bfs(initial: T,
        goal_test: Callable[[T], bool],
        successors: Callable[[T], List[T]]) -> Tuple[Optional[Node[T]], int]:
    # frontier는 아직 방문하지 않은 곳
    frontier: Queue[Node[T]] = Queue()
    frontier.push(Node(initial, None))
    # explored는 이미 방문한 곳
    explored: Set[T] = {initial}

    visited_count: int = 0  # 🔹 탐색한 지점 수

    # 방문할 곳이 더 있는지 탐색
    while not frontier.empty:
        current_node: Node[T] = frontier.pop()
        visited_count += 1
        current_state: T = current_node.state
        # 목표 지점을 찾았다면 종료
        if goal_test(current_state):
            return current_node, visited_count
        # 방문하지 않은 다음 장소가 있는지 확인
        for child in successors(current_state):
            if child in explored:
                continue
            explored.add(child)
            frontier.push(Node(child, current_node))
    return None, visited_count

class PriorityQueue(Generic[T]):
    def __init__(self) -> None:
        self._container: List[T] = []
    
    @property
    def empty(self) -> bool:
        return not self._container
    
    def push(self, item: T) -> None:
        heappush(self._container, item) # 우선순위 push

    def pop(self) -> T:
        return heappop(self._container) # 우선순위 pop

    def __repr__(self) -> str:
        return repr(self._container)

# def astar(initial: T, goal_test: Callable[[T], bool], successors: Callable[[T], List[T]], heuristic: Callable[[T], float]) -> Optional[Node[T]]:
#     # frontier는 방문하지 않은 곳
#     frontier: PriorityQueue[Node[T]] = PriorityQueue()
#     frontier.push(Node(initial, None, 0.0, heuristic(initial)))
#     # explored는 이미 방문한 곳
#     explored: Dict[T, float] = {initial: 0.0}

#     # 방문할 곳이 더 있는지 탐색
#     while not frontier.empty:
#         current_node: Node[T] = frontier.pop()
#         current_state: T = current_node.state
#         # 목표 지점을 찾았다면 종료
#         if goal_test(current_state):
#             return current_node
#         # 방문하지 않은 다음 장소가 있는지 확인    
#         for child in successors(current_state):
#             # 현재 장소에서 갈 수 있는 다음 장소의 비용은 1이라고 가정
#             new_cost: float = current_node.cost + 1

#             if child not in explored or explored[child] > new_cost:
#                 explored[child] = new_cost
#                 frontier.push(Node(child, current_node, new_cost, heuristic(child)))
#     return None # 모든 곳을 방문했지만 결국 목표 지점을 찾지 못함

# counter 추가
def astar(initial: T,
          goal_test: Callable[[T], bool],
          successors: Callable[[T], List[T]],
          heuristic: Callable[[T], float]) -> Tuple[Optional[Node[T]], int]:
    # frontier는 방문하지 않은 곳
    frontier: PriorityQueue[Node[T]] = PriorityQueue()
    frontier.push(Node(initial, None, 0.0, heuristic(initial)))
    # explored는 이미 방문한 곳 (각 state까지의 최소 cost)
    explored: Dict[T, float] = {initial: 0.0}

    visited_count: int = 0  # 🔹 탐색한 지점 수

    # 방문할 곳이 더 있는지 탐색
    while not frontier.empty:
        current_node: Node[T] = frontier.pop()
        visited_count += 1
        current_state: T = current_node.state
        # 목표 지점을 찾았다면 종료
        if goal_test(current_state):
            return current_node, visited_count
        # 방문하지 않은 다음 장소가 있는지 확인    
        for child in successors(current_state):
            # 현재 장소에서 갈 수 있는 다음 장소의 비용은 1이라고 가정
            new_cost: float = current_node.cost + 1

            if child not in explored or explored[child] > new_cost:
                explored[child] = new_cost
                frontier.push(Node(child, current_node, new_cost, heuristic(child)))
    return None, visited_count

if __name__ == "__main__":
    print(linear_contains([1, 5, 15, 15, 15, 15, 20], 5))
    print(binary_contains(["a", "d,", "e", "f", "z"], "f"))
    print(binary_contains(["john", "mark", "ronald", "sarah"], "sheila"))
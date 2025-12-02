from typing import TypeVar, List, Set
from graph import Graph  # 네가 만든 Graph 사용

V = TypeVar("V")

def vertex_degrees(g: Graph[V]) -> List[int]:
    """각 정점의 차수(degree) 리스트를 반환."""
    degrees: List[int] = []
    for i in range(g.vertex_count):
        degrees.append(len(g.edges_for_index(i)))
    return degrees

def is_connected_ignoring_isolated(g: Graph[V]) -> bool:
    """
    차수가 0인 정점(고립된 정점)은 무시하고,
    나머지 정점들이 하나의 연결 요소를 이루는지 확인.
    """
    # 차수 > 0 인 정점만 대상으로 함
    non_isolated_indices = [i for i in range(g.vertex_count)
                            if len(g.edges_for_index(i)) > 0]
    if not non_isolated_indices:
        # 에지가 하나도 없는 그래프는 연결된 것으로 간주 (여기선 해당 없음)
        return True

    # DFS/스택을 이용하여 연결성 검사
    start = non_isolated_indices[0]
    visited: Set[int] = set()
    stack: List[int] = [start]

    while stack:
        current = stack.pop()
        if current in visited:
            continue
        visited.add(current)
        # 이웃 정점 인덱스들
        for v in [g.index_of(nbr) for nbr in g.neighbors_for_index(current)]:
            if len(g.edges_for_index(v)) > 0 and v not in visited:
                stack.append(v)

    # 차수 > 0 인 정점들이 모두 방문되었는지 확인
    return visited == set(non_isolated_indices)

def analyze_eulerian(g: Graph[V]) -> None:
    """그래프가 오일러 경로/회로를 가지는지 분석하고 출력."""
    degs = vertex_degrees(g)
    print("정점별 차수:")
    for i in range(g.vertex_count):
        print(f"  {g.vertex_at(i)}: degree = {degs[i]}")
    print()

    connected = is_connected_ignoring_isolated(g)
    odd_vertices = [g.vertex_at(i) for i, d in enumerate(degs) if d % 2 == 1]

    print(f"연결 그래프 여부(차수>0인 정점 대상으로): {connected}")
    print(f"홀수 차수 정점들: {odd_vertices}")
    print(f"홀수 차수 정점 개수: {len(odd_vertices)}")
    print()

    if not connected:
        print("=> 연결 그래프가 아니므로 오일러 경로/회로가 존재할 수 없습니다.")
        return

    if len(odd_vertices) == 0:
        print("=> 모든 정점 차수가 짝수이므로 오일러 회로가 존재합니다.")
    elif len(odd_vertices) == 2:
        print("=> 정확히 2개의 정점만 홀수 차수이므로 오일러 경로는 존재하지만 회로는 없습니다.")
        print(f"   (시작 정점 후보: {odd_vertices[0]}, 끝 정점 후보: {odd_vertices[1]})")
    else:
        print("=> 홀수 차수 정점이 0개도 2개도 아니므로")
        print("   오일러 경로/오일러 회로 모두 존재하지 않습니다.")

if __name__ == "__main__":
    # 위키피디아에 나오는 쾨니히스베르크 다리 모델
    #
    # 보통 4개의 육지(정점)과 7개의 다리(에지)로 나타냄.
    # A: 북쪽 육지
    # B: 남쪽 육지
    # C: 서쪽 섬
    # D: 동쪽 섬
    #
    # 위키 기준 그래프 모델 중 하나:
    #   - A-B 다리 2개
    #   - A-C 다리 1개
    #   - A-D 다리 1개
    #   - B-D 다리 1개
    #   - C-D 다리 2개
    #
    # 이 그래프의 각 정점 차수는:
    #   A: 4, B: 3, C: 3, D: 5  (모든 정점이 홀수 → 오일러 경로 없음)

    vertices = ["A", "B", "C", "D"]
    g: Graph[str] = Graph(vertices)

    # A-B (2개)
    g.add_edge_by_vertices("A", "B")
    g.add_edge_by_vertices("A", "B")

    # A-C (1개)
    g.add_edge_by_vertices("A", "C")

    # A-D (1개)
    g.add_edge_by_vertices("A", "D")

    # B-D (1개)
    g.add_edge_by_vertices("B", "D")

    # C-D (2개)
    g.add_edge_by_vertices("C", "D")
    g.add_edge_by_vertices("C", "D")

    print("쾨니히스베르크 그래프:")
    print(g)
    print("-" * 50)

    analyze_eulerian(g)

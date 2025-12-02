from typing import TypeVar, Generic, List
from edge import Edge
from graph import Graph

V = TypeVar("V")

class DirectedGraph(Generic[V], Graph[V]):
    def __init__(self, vertices: List[V] = None) -> None:
        if vertices is None:
            vertices = []
        # Graph 초기화
        self._vertices: List[V] = vertices
        self._edges: List[List[Edge]] = [[] for _ in vertices]

    # 무향 그래프와 다르게 reversed()를 추가하지 않는다!
    def add_edge(self, edge: Edge) -> None:
        self._edges[edge.u].append(edge)

    def add_edge_by_indices(self, u: int, v: int) -> None:
        edge = Edge(u, v)
        self.add_edge(edge)

    def add_edge_by_vertices(self, first: V, second: V) -> None:
        u = self._vertices.index(first)
        v = self._vertices.index(second)
        self.add_edge_by_indices(u, v)

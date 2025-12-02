from typing import TypeVar, Generic, List, Tuple
from graph import Graph
from weighted_edge import WeightedEdge

V = TypeVar('V')

class WeightedDirectedGraph(Generic[V], Graph[V]):
    def __init__(self, vertices: List[V] = None) -> None:
        if vertices is None:
            vertices = []
        self._vertices: List[V] = vertices
        self._edges: List[List[WeightedEdge]] = [[] for _ in vertices]

    # 🔴 유향 그래프: u -> v 한 방향만 추가
    def add_edge(self, edge: WeightedEdge) -> None:
        self._edges[edge.u].append(edge)

    def add_edge_by_indices(self, u: int, v: int, weight: float) -> None:
        edge = WeightedEdge(u, v, weight)
        self.add_edge(edge)

    def add_edge_by_vertices(self, first: V, second: V, weight: float) -> None:
        u = self._vertices.index(first)
        v = self._vertices.index(second)
        self.add_edge_by_indices(u, v, weight)

    def neighbors_for_index_with_weights(self, index: int) -> List[Tuple[V, float]]:
        distance_tuples: List[Tuple[V, float]] = []
        for edge in self._edges[index]:
            distance_tuples.append((self.vertex_at(edge.v), edge.weight))
        return distance_tuples

    def __str__(self) -> str:
        desc = ""
        for i in range(self.vertex_count):
            desc += f"{self.vertex_at(i)} -> {self.neighbors_for_index_with_weights(i)}\n"
            # 예: Seattle -> [('Chicago', 1737.0), ('SF', 678.0)]
        return desc

if __name__ == "__main__":
    city_graph3 = WeightedDirectedGraph[str]([
        "Seattle", "San Francisco", "Los Angeles", "Riverside", "Phoenix"
    ])

    # 단방향 간선: Seattle -> SF, SF -> LA, LA -> Phoenix ...
    city_graph3.add_edge_by_vertices("Seattle", "San Francisco", 678)
    city_graph3.add_edge_by_vertices("San Francisco", "Los Angeles", 348)
    city_graph3.add_edge_by_vertices("Los Angeles", "Phoenix", 357)
    city_graph3.add_edge_by_vertices("Phoenix", "Seattle", 1100)  # 역방향 따로 추가

    print(city_graph3)

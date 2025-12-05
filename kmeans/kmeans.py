from __future__ import annotations
from typing import TypeVar, Generic, List, Sequence
from copy import deepcopy
from functools import partial
from random import uniform
from statistics import mean, pstdev
from dataclasses import dataclass
from data_point import DataPoint

def zscores(original: Sequence[float]) -> List[float]:
    avg: float = mean(original)
    std: float = pstdev(original)
    if std == 0: # 변화 차이가 없으면 모두 0으로 반환
        return [0] * len(original)
    return [(x - avg) / std for x in original]

Point = TypeVar('Point', bound=DataPoint)

class KMeans(Generic[Point]):
    @dataclass
    class Cluster:
        points: List[Point]
        centroid: DataPoint
    
    def __init__(self, k: int, points: List[Point]) -> None:
        if k < 1: # k-평균은 음수 또는 0인 군집에는 동작하지 않음
            raise ValueError("k must be >= 1")
        self._points: List[Point] = points
        self._zscore_normalize()
        # 임의의 중심으로 빈 군집을 초기화
        self._clusters: List[KMeans.Cluster] = []
        for _ in range(k):
            rand_point: DataPoint = self._random_point()
            cluster: KMeans.Cluster = KMeans.Cluster([], rand_point)
            self._clusters.append(cluster)

    @property
    def _centroids(self) -> List[DataPoint]:
        return [x.centroid for x in self._clusters]

    def _dimension_slice(self, dimension: int) -> List[float]:
        return [x.dimensions[dimension] for x in self._points]

    def _zscore_normalize(self) -> None:
        zscored: List[List[float]] = [[] for _ in range(len(self._points))]
        for dimension in range(self._points[0].num_dimensions):
            dimension_slice: List[float] = self._dimension_slice(dimension)
            for index, zscore in enumerate(zscores(dimension_slice)):
                zscored[index].append(zscore)
        for i in range(len(self._points)):
            self._points[i].dimensions = tuple(zscored[i])

    def _random_point(self) -> DataPoint:
        rand_dimensions: List[float] = []
        for dimension in range(self._points[0].num_dimensions):
            values: List[float] = self._dimension_slice(dimension)
            rand_value: float = uniform(min(values), max(values))
            rand_dimensions.append(rand_value)

        return DataPoint(rand_dimensions)

    # 각 포인트에 가장 가까운 군집 중심을 찾아 해당 군집에 포인트를 할당
    def _assign_clusters(self) -> None:
        for point in self._points:
            closet: DataPoint = min(self._centroids, key=partial(DataPoint.distance, point))
            idx: int = self._centroids.index(closet)
            cluster: KMeans.Cluster = self._clusters[idx]
            cluster.points.append(point)

    # 각 군집의 중심을 찾아서 그곳으로 중심을 옮김
    def _generate_centroids(self) -> None:
        for cluster in self._clusters:
            if len(cluster.points) == 0: # 포인트가 없으면 같은 중심으로 유지
                continue
            means: List[float] = []
            for dimension in range(cluster.points[0].num_dimensions):
                dimension_slice: List[float] = [p.dimensions[dimension] for p in cluster.points]
                means.append(mean(dimension_slice))
            cluster.centroid = DataPoint(means)

    def run(self, max_iterations: int = 100) -> List[KMeans.Cluster]:
        for iteration in range(max_iterations):
            for cluster in self._clusters: # 모든 군집을 비움
                cluster.points.clear()
            self._assign_clusters() # 각 포인트에서 가장 가까운 군집을 찾음
            old_centroids: List[DataPoint] = deepcopy(self._centroids) # 중심을 복사
            self._generate_centroids() # 새로운 중심을 찾음
            if old_centroids == self._centroids: # 중심이 이동했는가?
                print(f"{iteration}회 반복 후 수렴")
                return self._clusters
        return self._clusters

if __name__ == "__main__":
    point1: DataPoint = DataPoint([2.0, 1.0, 1.0])
    point2: DataPoint = DataPoint([2.0, 2.0, 5.0])
    point3: DataPoint = DataPoint([3.0, 1.5, 2.5])
    kmeans_test: KMeans[DataPoint] = KMeans(2, [point1, point2, point3])
    test_clusters: List[KMeans.Cluster] = kmeans_test.run()
    for index, cluster in enumerate(test_clusters):
        print(f"군집 {index}: {cluster.points}")
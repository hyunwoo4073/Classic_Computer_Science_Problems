from __future__ import annotations
from typing import Iterator, Tuple, List, Iterable
from math import sqrt
import csv

class DataPoint:
    def __init__(self, initial: Iterable[float]) -> None:
        self._originals: Tuple[float, ...] = tuple(initial)
        self.dimensions: Tuple[float, ...] = tuple(initial)

    @property
    def num_dimensions(self) -> int:
        return len(self.dimensions)

    def distance(self, other: DataPoint) -> float:
        combined: Iterator[Tuple[float, float]] = zip(self.dimensions, other.dimensions)
        difference: List[float] = [(x - y) ** 2 for x, y in combined]
        return sqrt(sum(difference))

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, DataPoint):
            return NotImplemented
        return self.dimensions == other.dimensions

    def __repr__(self) -> str:
        return self._originals.__repr__()

    @staticmethod
    def from_csv(filepath: str, skip_header: bool = True) -> List["DataPoint"]:
        datapoints: List[DataPoint] = []

        with open(filepath, "r", newline="", encoding="utf-8") as f:
            reader = csv.reader(f)

            # 첫 줄 헤더 스킵
            if skip_header:
                next(reader, None)

            for row in reader:
                if not row:
                    continue

                try:
                    values = [float(x) for x in row]
                except ValueError:
                    continue  # 숫자로 변환 불가하면 스킵

                datapoints.append(DataPoint(values))

        return datapoints
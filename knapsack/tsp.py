from typing import Dict, List, Iterable, Tuple
from itertools import permutations

vt_distances: Dict[str, Dict[str, int]] = {
    "러틀랜드":
        {"빌링턴": 67,
         "화이트 리버 정션": 46,
         "베닝턴": 55,
         "브래틀보로": 75},
    "빌링턴":
        {"러틀랜드": 67,
         "화이트 리버 정션": 91,
         "베닝턴": 122,
         "브래틀보로": 153},
    "화이트 리버 정션":
        {"러틀랜드": 46,
         "빌링턴": 91,
         "베닝턴": 98,
         "브래틀보로": 65},
    "베닝턴":
        {"러틀랜드": 55,
         "빌링턴": 122,
         "화이트 리버 정션": 98,
         "브래틀보로": 40},
    "브래틀보로":
        {"러틀랜드": 75,
         "빌링턴": 153,
         "화이트 리버 정션": 65,
         "베닝턴": 40}
}

vt_cities: Iterable[str] = vt_distances.keys()
city_permutations: Iterable[Tuple[str, ...]] = permutations(vt_cities)

tsp_paths: List[Tuple[str, ...]] = [c + (c[0],) for c in city_permutations]

if __name__ == "__main__":
    best_path: Tuple[str, ...]
    min_distance: int = 999999999999
    for path in tsp_paths:
        distance: int = 0
        last: str = path[0]
        for next in path[1:]:
            distance += vt_distances[last][next]
            last = next
        if distance < min_distance:
            min_distance = distance
            best_path = path
    print(f"최단 경로는 {best_path} 이고, {min_distance} 마일입니다.")
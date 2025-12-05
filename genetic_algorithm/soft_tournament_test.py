# from __future__ import annotations
# from typing import List, Tuple
# from collections import Counter
# from random import seed

# from chromosome import Chromosome
# from genetic_algorithm import GeneticAlgorithm

# # ---------------------------------------------------------
# # 간단한 염색체: 이름 + 고정된 fitness 값만 갖는 타입
# # ---------------------------------------------------------
# class SimpleChromosome(Chromosome):
#     def __init__(self, name: str, fit: float) -> None:
#         self.name = name
#         self._fit = fit

#     def fitness(self) -> float:
#         return self._fit

#     @classmethod
#     def random_instance(cls) -> SimpleChromosome:
#         # 이 데모에서는 사용하지 않음
#         return cls("X", 0.0)

#     def crossover(self, other: SimpleChromosome) -> Tuple[SimpleChromosome, SimpleChromosome]:
#         # 이 데모에서는 유전 연산이 목적이 아니므로 그대로 반환
#         return self, other

#     def mutate(self) -> None:
#         # 이 데모에서는 돌연변이도 사용하지 않음
#         pass

#     def __repr__(self) -> str:
#         return f"{self.name}(fit={self._fit})"


# def run_selection_experiment(
#     selection_type: GeneticAlgorithm.SelectionType,
#     label: str,
#     num_trials: int = 10_000,
# ) -> None:
#     # 1) 고정된 population 구성 (A가 제일 fitness가 높음)
#     population: List[SimpleChromosome] = [
#         SimpleChromosome("A", 10.0),  # 1등
#         SimpleChromosome("B", 9.0),   # 2등
#         SimpleChromosome("C", 8.0),   # 3등
#         SimpleChromosome("D", 7.0),
#         SimpleChromosome("E", 6.0),
#     ]

#     # 2) GA 인스턴스 생성
#     #    run()은 안 쓸 거고, 안에 있는 selection 메서드만 테스트용으로 호출
#     ga: GeneticAlgorithm[SimpleChromosome] = GeneticAlgorithm(
#         initial_population=population,
#         threshold=9999.0,            # 안 쓰는 값
#         max_generations=1,           # 안 쓸 거라 의미 없음
#         mutation_chance=0.0,
#         crossover_chance=1.0,
#         selection_type=selection_type,
#     )

#     # 3) 부모로 선택된 횟수를 카운트
#     parent_counter = Counter()

#     # 4) 여러 번 부모 선택 반복
#     for _ in range(num_trials):
#         if selection_type == GeneticAlgorithm.SelectionType.ROULETTE:
#             parents = ga._pick_roulette([x.fitness() for x in population])
#         elif selection_type == GeneticAlgorithm.SelectionType.TOURNAMENT:
#             # 하드 토너먼트: 참가자 3명 중 상위 2명
#             parents = ga._pick_tournament(num_participants=3)
#         else:
#             # 소프트 토너먼트:
#             # 너가 구현해 둔 _pick_soft_tournament 시그니처에 맞춰서 호출
#             # 예: def _pick_soft_tournament(self, num_participants: int, pressure: float = 1.5)
#             parents = ga._pick_soft_tournament(num_participants=3)

#         for p in parents:
#             parent_counter[p.name] += 1

#     # 5) 결과 출력
#     print(f"\n=== {label} ({num_trials}번 선택, 부모 2명씩) ===")
#     total_picks = sum(parent_counter.values())
#     for name in ["A", "B", "C", "D", "E"]:
#         cnt = parent_counter[name]
#         ratio = (cnt / total_picks * 100) if total_picks > 0 else 0.0
#         print(f"{name}: {cnt:6d}회 선택 ({ratio:5.2f}%)")


# if __name__ == "__main__":
#     # 재현 가능하게 랜덤 시드 고정
#     seed(42)

#     # 1) 하드 토너먼트
#     run_selection_experiment(
#         selection_type=GeneticAlgorithm.SelectionType.TOURNAMENT,
#         label="하드 토너먼트 선택"
#     )

#     # 2) 소프트 토너먼트
#     run_selection_experiment(
#         selection_type=GeneticAlgorithm.SelectionType.SOFT_TOURNAMENT,
#         label="소프트 토너먼트 선택"
#     )
from __future__ import annotations
from dataclasses import dataclass
from typing import List, Tuple
from random import choices, seed
from collections import Counter


@dataclass
class Individual:
    name: str
    fitness: float


# 하드 토너먼트: 참가자 중 상위 2명 "무조건" 선택
def hard_tournament(population: List[Individual], k: int) -> Tuple[Individual, Individual]:
    # k명 random 샘플링
    participants = choices(population, k=k)
    # fitness 내림차순 정렬 후 상위 2명
    sorted_participants = sorted(participants, key=lambda ind: ind.fitness, reverse=True)
    return sorted_participants[0], sorted_participants[1]


# 소프트 토너먼트: 순위 기반 가중치로 확률적으로 상위 개체를 더 자주 뽑음
def soft_tournament(
    population: List[Individual],
    k: int,
    pressure: float = 0.5,  # 0.0~1.0 근처: 상위 쏠림 완화, 1.5 이상: 상위에 더 쏠림
) -> Tuple[Individual, Individual]:
    participants = choices(population, k=k)
    # fitness 내림차순 정렬 (0번이 1등)
    sorted_participants = sorted(participants, key=lambda ind: ind.fitness, reverse=True)
    n = len(sorted_participants)

    # 순위 기반 weight: w(rank) = (n - rank)^pressure
    # rank=0(1등) -> (n)^pressure
    # rank가 커질수록 weight 줄어듦, pressure를 낮추면 더 평평해짐
    weights = [(n - rank) ** pressure for rank in range(n)]

    parent1, parent2 = choices(sorted_participants, weights=weights, k=2)
    return parent1, parent2


def run_experiment(num_trials: int = 10_000) -> None:
    # 재현 가능하도록 seed 고정
    seed(42)

    # fitness를 아주 극단적으로 설정 (차이 극대화)
    population: List[Individual] = [
        Individual("A", 100.0),
        Individual("B", 50.0),
        Individual("C", 20.0),
        Individual("D", 10.0),
        Individual("E", 5.0),
        Individual("F", 1.0),
        Individual("G", 1.0),
        Individual("H", 1.0),
        Individual("I", 1.0),
        Individual("J", 1.0),
    ]

    k = len(population)  # 토너먼트 참가자를 전체로 → 압력 극대화

    # ---- 하드 토너먼트 ----
    hard_counter = Counter()
    for _ in range(num_trials):
        p1, p2 = hard_tournament(population, k=k)
        hard_counter[p1.name] += 1
        hard_counter[p2.name] += 1

    # ---- 소프트 토너먼트 ----
    soft_counter = Counter()
    for _ in range(num_trials):
        p1, p2 = soft_tournament(population, k=k, pressure=0.4)  # pressure 낮게 → 다양성↑
        soft_counter[p1.name] += 1
        soft_counter[p2.name] += 1

    # ---- 결과 출력 ----
    print(f"\n=== 하드 토너먼트 (시행 {num_trials}회, 부모 2명씩) ===")
    total_hard = sum(hard_counter.values())
    for ind in population:
        cnt = hard_counter[ind.name]
        ratio = cnt / total_hard * 100 if total_hard > 0 else 0
        bar = "#" * (cnt * 50 // total_hard)  # 간단한 바 차트
        print(f"{ind.name}: {cnt:6d}회 ({ratio:5.2f}%) {bar}")

    print(f"\n=== 소프트 토너먼트 (시행 {num_trials}회, 부모 2명씩, pressure=0.4) ===")
    total_soft = sum(soft_counter.values())
    for ind in population:
        cnt = soft_counter[ind.name]
        ratio = cnt / total_soft * 100 if total_soft > 0 else 0
        bar = "#" * (cnt * 50 // total_soft)
        print(f"{ind.name}: {cnt:6d}회 ({ratio:5.2f}%) {bar}")


if __name__ == "__main__":
    run_experiment(num_trials=10_000)

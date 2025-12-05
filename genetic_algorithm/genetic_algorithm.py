from __future__ import annotations
from typing import TypeVar, Generic, List, Tuple, Callable
from enum import Enum
from random import choices, random 
from heapq import nlargest
from statistics import mean
from chromosome import Chromosome

C = TypeVar('C', bound=Chromosome) # 염색체 타입

class GeneticAlgorithm(Generic[C]):
    SelectionType = Enum("SelectionType", "ROULETTE TOURNAMENT SOFT_TOURNAMENT")

    def __init__(self, initial_population: List[C], threshold: float, max_generations: int = 100, mutation_chance: float = 0.01, crossover_chance: float = 0.7,
    selection_type: SelectionType = SelectionType.TOURNAMENT) -> None:
        self._population: List[C] = initial_population
        self._threshold: float = threshold
        self._max_generations: int = max_generations
        self._mutation_chance: float = mutation_chance
        self._crossover_chance: float = crossover_chance
        self._selection_type: GeneticAlgorithm.SelectionType = selection_type
        self._fitness_key: Callable = type(self._population[0]).fitness

    # 두 부모를 선택하기 위해 룰렛휠(확률 분포)을 사용
    # 메모: 음수 적합도와 작동하지 않음
    def _pick_roulette(self, wheel: List[float]) -> Tuple[C, C]:
        return tuple(choices(self._population, weights=wheel, k=2))

    # 무작위로 num_participants만큼 추출한 후 적합도가 가장 높은 두 염색체를 선택
    def _pick_tournament(self, num_participants: int) -> Tuple[C, C]:
        participants: List[C] = choices(self._population, k=num_participants)
        return tuple(nlargest(2, participants, key=self._fitness_key))
    
    # 고급(소프트) 토너먼트 선택:
    # - 참가자들을 fitness 기준으로 정렬
    # - 순위(1등, 2등, 3등...)에 따라 가중치 부여
    #   -> 1등이 가장 높은 확률이지만 2,3등도 non-zero 확률로 선택
    def _pick_soft_tournament(
        self,
        num_participants: int,
        pressure: float = 1.5,  # pressure↑면 1등 쏠림, pressure↓면 고르게
    ) -> Tuple[C, C]:
        # 토너먼트에 참가할 개체들을 무작위로 뽑음
        participants: List[C] = choices(self._population, k=num_participants)
        # fitness 기준 내림차순 정렬 (0번이 1등)
        sorted_participants: List[C] = sorted(
            participants, key=self._fitness_key, reverse=True
        )
        n = len(sorted_participants)

        # 순위 기반 가중치: w(rank) = (n - rank)^pressure
        # rank: 0(1등), 1(2등), ...
        # → 1등이 제일 크지만, 2/3등도 꽤 의미 있는 확률을 가짐
        weights: List[float] = [float((n - rank) ** pressure) for rank in range(n)]

        # random.choices 로 확률적으로 두 부모 선택
        # (같은 개체가 두 번 뽑일 수도 있지만, GA 에서는 보통 허용)
        parents: Tuple[C, C] = tuple(
            choices(sorted_participants, weights=weights, k=2)
        )  # type: ignore
        return parents

    # # 집단을 새로운 세대로 교체
    # def _reproduce_and_replace(self) -> None:
    #     new_population: List[C] = []
    #     # 새로운 세대가 채워질 때까지 반복
    #     while len(new_population) < len(self._population):
    #         # parents 중 두 부모를 선택
    #         if self._selection_type == GeneticAlgorithm.SelectionType.ROULETTE:
    #             parents: Tuple[C, C] = self._pick_roulette([x.fitness() for x in self._population])
    #         else:
    #             parents = self._pick_tournament(len(self._population) // 2)
    #         # 두 부모를 크로스오버
    #         if random() < self._crossover_chance:
    #             new_population.extend(parents[0].crossover(parents[1]))
    #         else:
    #             new_population.extend(parents)
    #     # 새 집단의 수가 홀수라면 이전 집단보다 하나 더 많으므로 제거
    #     if len(new_population) > len(self._population):
    #         new_population.pop()
    #     self._population = new_population # 새 집단으로 참조를 변경

    # 집단을 새로운 세대로 교체
    def _reproduce_and_replace(self) -> None:
        new_population: List[C] = []
        # 새로운 세대가 채워질 때까지 반복
        while len(new_population) < len(self._population):
            # parents 중 두 부모를 선택
            if self._selection_type == GeneticAlgorithm.SelectionType.ROULETTE:
                parents: Tuple[C, C] = self._pick_roulette(
                    [x.fitness() for x in self._population]
                )
            elif self._selection_type == GeneticAlgorithm.SelectionType.TOURNAMENT:
                parents = self._pick_tournament(len(self._population) // 2)
            else:
                # SOFT_TOURNAMENT
                parents = self._pick_soft_tournament(len(self._population) // 2)

            # 두 부모를 크로스오버
            if random() < self._crossover_chance:
                new_population.extend(parents[0].crossover(parents[1]))
            else:
                new_population.extend(parents)

        # 새 집단의 수가 홀수라면 이전 집단보다 하나 더 많으므로 제거
        if len(new_population) > len(self._population):
            new_population.pop()
        self._population = new_population  # 새 집단으로 참조를 변경

    # _mutation_chance 확률로 각 개발 염색체를 돌연변이함
    def _mutate(self) -> None:
        for individual in self._population:
            if random() < self._mutation_chance:
                individual.mutate()

    # max_generations만큼 유전 알고리즘을 실행하고,
    # 최상의 적합도를 가진 개체를 반환
    def run(self) -> C:
        best: C = max(self._population, key=self._fitness_key)
        for generation in range(self._max_generations):
            # 임곗값을 초과하면 개체를 바로 반환
            if best.fitness() >= self._threshold:
                return best
            print(f"세대 {generation} 최상 {best.fitness()} 평균 {mean(map(self._fitness_key, self._population))}")
            self._reproduce_and_replace()
            self._mutate()
            highest: C = max(self._population, key=self._fitness_key)
            if highest.fitness() > best.fitness():
                best = highest # 새로운 최상의 개체를 발견
        return best # _max_generations에서 발견한 최상의 개체를 반환
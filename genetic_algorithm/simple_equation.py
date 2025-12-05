from __future__ import annotations
from typing import Tuple, List
from chromosome import Chromosome
from genetic_algorithm import GeneticAlgorithm
from random import randrange, random
from copy import deepcopy
from bit_string import BitString

class SimpleEquation(Chromosome):
    def __init__(self, x: int, y: int) -> None:
        self.x: int = x
        self.y: int = y

    def fitness(self) -> float: # 6x - x^2 + 4y -y^2
        return 6 * self.x - self.x * self.x + 4 * self.y - self.y * self.y

    @classmethod
    def random_instance(cls) -> SimpleEquation:
        return SimpleEquation(randrange(100), randrange(100))

    def crossover(self, other: SimpleEquation) -> Tuple[SimpleEquation, SimpleEquation]:
        child1: SimpleEquation = deepcopy(self)
        child2: SimpleEquation = deepcopy(other)
        child1.y = other.y
        child2.y = self.y
        return child1, child2

    def mutate(self) -> None:
        if random() > 0.5: # x를 돌연변이함
            if random() > 0.5:
                self.x += 1
            else:
                self.x -= 1
        else: # 그렇지 않으면 y를 돌연변이함
            if random() > 0.5:
                self.y += 1
            else:
                self.y -= 1

    def __str__(self) -> str:
        return f"X: {self.x} Y: {self.y} 적합도: {self.fitness()}"

if __name__ == "__main__":
    # initial_population: List[SimpleEquation] = [SimpleEquation.random_instance() for _ in range(20)]
    # ga: GeneticAlgorithm[SimpleEquation] = GeneticAlgorithm(initial_population=initial_population, threshold=13.0, max_generations=100, mutation_chance=0.1, crossover_chance=0.7)
    # result: SimpleEquation = ga.run()
    # print(result)

    # 초기 개체 집단
    initial_population: List[BitString] = [
        BitString.random_instance() for _ in range(50)
    ]

    # f(x, y)의 최대값 13에 맞춰 threshold를 13.0으로
    ga: GeneticAlgorithm[BitString] = GeneticAlgorithm(
        initial_population=initial_population,
        threshold=13.0,
        max_generations=200,
        mutation_chance=0.1,
        crossover_chance=0.7,
        # roulette은 음수 fitness에서 문제될 수 있으니 토너먼트 계열 추천
        selection_type=GeneticAlgorithm.SelectionType.TOURNAMENT,
        # 또는 SOFT_TOURNAMENT 써도 됨
        # selection_type=GeneticAlgorithm.SelectionType.SOFT_TOURNAMENT,
    )

    result: BitString = ga.run()
    print(result)
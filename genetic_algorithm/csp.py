from typing import Generic, TypeVar, Dict, List, Optional
from abc import ABC, abstractmethod

from chromosome import Chromosome
from genetic_algorithm import GeneticAlgorithm

V = TypeVar('V')  # 변수(Variable) 타입
D = TypeVar('D')  # 도메인(Domain) 타입

# 모든 제약 조건에 대한 베이스 클래스
class Constraint(Generic[V, D], ABC):
    # 제약 조건 변수
    def __init__(self, variables: List[V]) -> None:
        self.variables = variables

    # 서브클래스 메서드에 의해 오버라이드
    @abstractmethod
    def satisfied(self, assignment: Dict[V, D]) -> bool:
        ...


# 제약 충족 문제는 타입 V의 '변수'와 범위를 나타내는 타입 D의 '도메인'
# 특정 변수의 도메인이 유효한지 확인하는 제약 조건으로 구성됨
class CSP(Generic[V, D]):
    def __init__(self, variables: List[V], domains: Dict[V, List[D]]) -> None:
        self.variables: List[V] = variables  # 제약 조건을 확인할 변수
        self.domains: Dict[V, List[D]] = domains  # 각 변수의 도메인
        self.constraints: Dict[V, List[Constraint[V, D]]] = {}
        for variable in self.variables:
            self.constraints[variable] = []
            if variable not in self.domains:
                raise LookupError("모든 변수에 도메인이 할당되어야 합니다.")

    def add_constraint(self, constraint: Constraint[V, D]) -> None:
        for variable in constraint.variables:
            if variable not in self.variables:
                raise LookupError("제약 조건 변수가 아닙니다.")
            else:
                self.constraints[variable].append(constraint)

    # 주어진 변수의 모든 제약 조건을 검사하여 assignment 값이 일관적인지 확인
    def consistent(self, variable: V, assignment: Dict[V, D]) -> bool:
        for constraint in self.constraints[variable]:
            if not constraint.satisfied(assignment):
                return False
        return True

    def backtracking_search(self, assignment: Dict[V, D] = {}) -> Optional[Dict[V, D]]:
        # assignment는 모든 변수가 할당될 때 완료(기저 조건)
        if len(assignment) == len(self.variables):
            return assignment

        # 할당되지 않은 모든 변수를 가져옴
        unassigned: List[V] = [v for v in self.variables if v not in assignment]

        # 할당되지 않은 첫 번째 변수의 가능한 모든 도메인 값을 가져옴
        first: V = unassigned[0]
        for value in self.domains[first]:
            local_assignment = assignment.copy()
            local_assignment[first] = value
            # local_assignment 값이 일관적이면 재귀 호출함
            if self.consistent(first, local_assignment):
                result: Optional[Dict[V, D]] = self.backtracking_search(local_assignment)
                # 결과를 찾지 못하면 백트래킹 종료
                if result is not None:
                    return result
        return None  # 솔루션 없음

    # --------------------- 여기부터 GA 기반 풀이 메서드 --------------------- #
    def solve_with_genetic_algorithm(
        self,
        population_size: int = 200,
        max_generations: int = 500,
        mutation_chance: float = 0.1,
        crossover_chance: float = 0.7,
        selection_type: GeneticAlgorithm.SelectionType = GeneticAlgorithm.SelectionType.TOURNAMENT,
    ) -> Optional[Dict[V, D]]:
        """
        유전 알고리즘을 사용해서 CSP를 근사적으로 푸는 메서드.
        - 염색체 = 변수 전체에 대한 하나의 완전한 할당(assignment)
        - 적합도 = 만족된 제약 조건의 수
        - 모든 제약을 만족하는 해를 찾으면 즉시 반환, 아니면 가장 좋은 해를 기준으로 판단
        """

        from random import choice, randrange

        # CSP 전체 제약 리스트 (각 constraint가 여러 변수에 중복 등록되어 있으므로 중복 제거)
        all_constraints = list({
            c for clist in self.constraints.values() for c in clist
        })
        total_constraints = len(all_constraints)

        # --- 염색체 정의: CSP에 대한 하나의 완전 할당 --- #
        class CSPChromosome(Chromosome):
            def __init__(self, assignment: Dict[V, D]) -> None:
                self.assignment = assignment  # 변수 -> 값 매핑

            def fitness(self) -> float:
                # 이 염색체가 만족시키는 제약 조건의 개수
                satisfied_count = 0
                for constraint in all_constraints:
                    # constraint.satisfied는 부분 할당도 받을 수 있게 설계되어 있으므로,
                    # 여기서는 전체 assignment를 그대로 전달
                    if constraint.satisfied(self.assignment):
                        satisfied_count += 1
                return float(satisfied_count)

            @classmethod
            def random_instance(cls) -> "CSPChromosome":
                # 각 변수에 대해 도메인에서 랜덤하게 값 하나 선택
                assignment: Dict[V, D] = {}
                for var in self.variables:  # 외부 CSP 인스턴스(self)에 클로저로 접근
                    domain_values = self.domains[var]
                    assignment[var] = choice(domain_values)
                return CSPChromosome(assignment)

            def crossover(
                self, other: "CSPChromosome"
            ) -> tuple["CSPChromosome", "CSPChromosome"]:
                # 간단한 균등(유니폼) 교차: 각 변수마다 50% 확률로 부모 값 스왑
                child1_assignment = self.assignment.copy()
                child2_assignment = other.assignment.copy()

                for var in self.variables:
                    if randrange(2) == 0:  # 0 또는 1
                        child1_assignment[var], child2_assignment[var] = (
                            child2_assignment[var],
                            child1_assignment[var],
                        )
                return CSPChromosome(child1_assignment), CSPChromosome(child2_assignment)

            def mutate(self) -> None:
                # 임의의 변수 하나를 골라 도메인에서 다른 값으로 바꿈
                var_index = randrange(len(self.variables))
                var = self.variables[var_index]
                domain_values = self.domains[var]
                old_value = self.assignment[var]
                # 도메인에 값이 하나뿐이면 바꿀 게 없음
                if len(domain_values) <= 1:
                    return
                # 기존 값과 다른 값 하나 고르기
                new_value = old_value
                while new_value == old_value:
                    new_value = choice(domain_values)
                self.assignment[var] = new_value

            def __str__(self) -> str:
                return f"Assignment({self.assignment}), fitness={self.fitness()}"

        # --- 초기 집단 구성 --- #
        initial_population: List[CSPChromosome] = [
            CSPChromosome.random_instance() for _ in range(population_size)
        ]

        # 적합도 임계값 = 모든 제약을 만족하는 경우
        threshold = float(total_constraints)

        ga: GeneticAlgorithm[CSPChromosome] = GeneticAlgorithm(
            initial_population=initial_population,
            threshold=threshold,
            max_generations=max_generations,
            mutation_chance=mutation_chance,
            crossover_chance=crossover_chance,
            selection_type=selection_type,
        )

        best: CSPChromosome = ga.run()

        # 모든 제약을 만족하는 해를 찾았는지 확인
        if best.fitness() == threshold:
            # 완전한 해
            return best.assignment
        else:
            # 완전한 해는 못 찾았지만, 가장 많은 제약을 만족하는 해를 볼 수도 있음
            # 여기서는 None을 돌려서 "완전한 해 없음"을 명확히 하고,
            # 필요하면 best.assignment를 반환하도록 바꿔도 됨.
            # return best.assignment  # <- 근사 해도 보고 싶다면 이 줄 사용
            return None

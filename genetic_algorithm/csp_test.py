from typing import Dict, List
from csp import CSP, Constraint


# ---------------------------
# 1. 제약 조건 정의
# ---------------------------
class AllDifferentConstraint(Constraint[str, int]):
    def __init__(self, variables: List[str]):
        super().__init__(variables)

    def satisfied(self, assignment: Dict[str, int]) -> bool:
        # 부분 할당에서는 아직 비교할 게 없을 수도 있음 → OK
        assigned_values = []
        for var in self.variables:
            if var in assignment:
                val = assignment[var]
                if val in assigned_values:  # 이미 나온 값이면 제약 위반
                    return False
                assigned_values.append(val)
        return True


# ---------------------------
# 2. 테스트 실행
# ---------------------------
if __name__ == "__main__":
    # 변수 및 도메인
    variables = ["A", "B", "C"]
    domains = {
        "A": [1, 2, 3],
        "B": [1, 2, 3],
        "C": [1, 2, 3],
    }

    # CSP 생성
    csp = CSP(variables, domains)

    # 제약 조건 추가 (A, B, C 모두 달라야 한다)
    csp.add_constraint(AllDifferentConstraint(["A", "B", "C"]))

    # -------------------------
    # Backtracking 방식 테스트
    # -------------------------
    print("=== Backtracking 결과 ===")
    solution_bt = csp.backtracking_search()
    print(solution_bt)

    # -------------------------
    # GA 방식 테스트
    # -------------------------
    print("\n=== Genetic Algorithm 결과 ===")
    solution_ga = csp.solve_with_genetic_algorithm(
        population_size=200,
        max_generations=500,
        mutation_chance=0.2,
        crossover_chance=0.7,
    )
    print(solution_ga)

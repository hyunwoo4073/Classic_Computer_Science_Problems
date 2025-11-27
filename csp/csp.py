from typing import Generic, TypeVar, Dict, List, Optional
from abc import ABC, abstractmethod

V = TypeVar('V') # 변수(Variable) 타입
D = TypeVar('D') # 도메인(Domain) 타입

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
        self.variables: List[V] = variables # 제약 조건을 확인할 변수
        self.domains: Dict[V, List[D]] = domains # 각 변수의 도메인
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
        return None # 솔루션 없음

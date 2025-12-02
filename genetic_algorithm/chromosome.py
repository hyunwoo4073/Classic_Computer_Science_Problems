from __future__ import annotations
from typing import TypeVar, Tuple, Type
from abc import ABC, abstractmethod

T = TypeVar('T', bound='Chromosome') # 자신을 반환하기 위해서 사용

# 모든 염색체의 베이스 클래스, 모든 메서드는 오버라이드됨
class Chromosome(ABC):
    @abstractmethod
    def fitness(self) -> float:
        ...
    
    @classmethod
    @abstractmethod
    def random_instance(cls: Type[T]) -> T:
        ...
    
    @abstractmethod
    def crossover(self: T, other: T) -> Tuple[T, T]:
        ...

    @abstractmethod
    def mutate(self) -> None:
        ...


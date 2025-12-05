# from __future__ import annotations
# from typing import List, Tuple
# from random import randint
# from chromosome import Chromosome  # 네가 올린 베이스 클래스

# class BitString(Chromosome):
#     # x, y 각각 6비트 → 0~63 표현 가능
#     GENE_LENGTH = 6
#     BIT_LENGTH = GENE_LENGTH * 2  # x용 6비트 + y용 6비트 = 12비트

#     def __init__(self, bits: List[int]) -> None:
#         # 0/1로 이뤄진 비트 리스트
#         self.bits = bits

#     # ---- 유틸리티: 비트열 <-> 정수 ----
#     @staticmethod
#     def _bits_to_int(bits: List[int]) -> int:
#         value = 0
#         for b in bits:
#             value = (value << 1) | b  # 왼쪽 쉬프트 후 최하위 비트에 b OR
#         return value

#     def decode(self) -> Tuple[int, int]:
#         """
#         bits[0:6] → x, bits[6:12] → y 로 해석
#         """
#         x_bits = self.bits[:self.GENE_LENGTH]
#         y_bits = self.bits[self.GENE_LENGTH:]
#         x = self._bits_to_int(x_bits)
#         y = self._bits_to_int(y_bits)
#         return x, y

#     # ---- Chromosome 추상 메서드 구현 ----
#     def fitness(self) -> float:
#         """
#         예제 문제: x + y = 42 에 가깝게 만들기
#         적합도 = 1 / ( |(x+y) - 42| + 1 )
#         → 정확히 42면 fitness = 1.0
#         → 멀어질수록 fitness가 0에 가까워짐
#         """
#         x, y = self.decode()
#         diff = abs((x + y) - 42)
#         return 1.0 / (diff + 1.0)

#     @classmethod
#     def random_instance(cls) -> BitString:
#         """
#         무작위 비트열 생성
#         """
#         bits = [randint(0, 1) for _ in range(cls.BIT_LENGTH)]
#         return BitString(bits)

#     def crossover(self, other: BitString) -> Tuple[BitString, BitString]:
#         """
#         한 점(single-point) 교차:
#         0과 BIT_LENGTH 사이에서 임의의 지점 하나를 선택해서
#         그 앞/뒤를 서로 교환
#         """
#         point = randint(1, self.BIT_LENGTH - 1)
#         child1_bits = self.bits[:point] + other.bits[point:]
#         child2_bits = other.bits[:point] + self.bits[point:]
#         return BitString(child1_bits), BitString(child2_bits)

#     def mutate(self) -> None:
#         """
#         비트 하나를 골라 0 <-> 1 플립
#         (실제 돌연변이 발생 빈도는 GA 쪽 mutation_chance가 결정)
#         """
#         idx = randint(0, self.BIT_LENGTH - 1)
#         self.bits[idx] = 1 - self.bits[idx]

#     def __str__(self) -> str:
#         x, y = self.decode()
#         s_bits = "".join(str(b) for b in self.bits)
#         return f"bits={s_bits} -> x={x}, y={y}, x+y={x+y}, fitness={self.fitness():.4f}"


from __future__ import annotations
from typing import List, Tuple
from random import randint
from chromosome import Chromosome  # 네가 올린 베이스 클래스

class BitString(Chromosome):
    # x, y 각각 6비트 → 0~63 표현 가능
    GENE_LENGTH = 6
    BIT_LENGTH = GENE_LENGTH * 2  # x용 6비트 + y용 6비트 = 12비트

    def __init__(self, bits: List[int]) -> None:
        # 0/1로 이뤄진 비트 리스트
        self.bits = bits

    # ---- 유틸리티: 비트열 <-> 정수 ----
    @staticmethod
    def _bits_to_int(bits: List[int]) -> int:
        value = 0
        for b in bits:
            value = (value << 1) | b  # 왼쪽 쉬프트 후 최하위 비트에 b OR
        return value

    def decode(self) -> Tuple[int, int]:
        """
        bits[0:6] → x, bits[6:12] → y 로 해석
        """
        x_bits = self.bits[:self.GENE_LENGTH]
        y_bits = self.bits[self.GENE_LENGTH:]
        x = self._bits_to_int(x_bits)
        y = self._bits_to_int(y_bits)
        return x, y

    # ---- Chromosome 추상 메서드 구현 ----
    def fitness(self) -> float:
        """
        단순 방정식 문제:
        f(x, y) = 6x - x^2 + 4y - y^2  (최대값 13, x=3, y=2)
        """
        x, y = self.decode()
        return 6 * x - x * x + 4 * y - y * y

    @classmethod
    def random_instance(cls) -> "BitString":
        """
        무작위 비트열 생성
        """
        bits = [randint(0, 1) for _ in range(cls.BIT_LENGTH)]
        return BitString(bits)

    def crossover(self, other: "BitString") -> Tuple["BitString", "BitString"]:
        """
        한 점(single-point) 교차:
        0과 BIT_LENGTH 사이에서 임의의 지점 하나를 선택해서
        그 앞/뒤를 서로 교환
        """
        point = randint(1, self.BIT_LENGTH - 1)
        child1_bits = self.bits[:point] + other.bits[point:]
        child2_bits = other.bits[:point] + self.bits[point:]
        return BitString(child1_bits), BitString(child2_bits)

    def mutate(self) -> None:
        """
        비트 하나를 골라 0 <-> 1 플립
        (실제 돌연변이 발생 빈도는 GA 쪽 mutation_chance가 결정)
        """
        idx = randint(0, self.BIT_LENGTH - 1)
        self.bits[idx] = 1 - self.bits[idx]

    def __str__(self) -> str:
        x, y = self.decode()
        s_bits = "".join(str(b) for b in self.bits)
        return f"bits={s_bits} -> x={x}, y={y}, f={self.fitness():.4f}"

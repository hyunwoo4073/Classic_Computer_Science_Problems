from enum import IntEnum
from typing import Tuple, List, Callable, Any
import time

Nucleotide: IntEnum = IntEnum('Nucleotide', ('A', 'C', 'G', 'T'))
Codon = Tuple[Nucleotide, Nucleotide, Nucleotide] # 코돈 타입 alias
Gene = List[Codon] # 유전자 타입 alias

def string_to_gene(s: str) -> Gene:
    gene: Gene = []
    for i in range(0, len(s), 3):
        if (i+2) >= len(s): # 현재 위치 다음에 2개의 문자가 없으면 실행하지 않음
            return gene
        # 3개의 뉴클레오타이드에서 코돈을 초기화
        codon: Codon = (Nucleotide[s[i]],
                        Nucleotide[s[i+1]], Nucleotide[s[i+2]])
        gene.append(codon) # 코돈을 유전자에 추가
    return gene

def linear_contains(gene: Gene, key_codon: Codon) -> bool:
    for codon in gene:
        if codon == key_codon:
            return True
    return False

gene_str: str = "ACGTGGCTCTCTAACGTACGTACGTACGGGGTTTATATATATACCCTAGGACTCCCTTT"
my_gene: Gene = string_to_gene(gene_str)

acg: Codon = (Nucleotide.A, Nucleotide.C, Nucleotide.G)
gat: Codon = (Nucleotide.G, Nucleotide.A, Nucleotide.T)
print(linear_contains(my_gene, acg)) # 참
print(linear_contains(my_gene, gat)) # 거짓

def binary_contains(gene: Gene, key_codon: Codon) -> bool:
    low: int = 0
    high: int = len(gene) - 1
    while low <= high: # 검색 공간(범위)이 있을 때까지 수행
        mid: int = (low + high) // 2
        if gene[mid] < key_codon:
            low = mid + 1
        elif gene[mid] > key_codon:
            high = mid - 1
        else:
            return True
    return False

def benchmark(func: Callable[[], Any], repeat: int = 1) -> float:
    start = time.perf_counter()
    for _ in range(repeat):
        func()
    end = time.perf_counter()
    return (end - start) / repeat

# 파이썬 표준 라이브러리 bisect 모듈을 사용하여 이진 검색 가능
my_sorted_gene: Gene = sorted(my_gene)
print(binary_contains(my_sorted_gene, acg))
print(binary_contains(my_sorted_gene, gat))


# 숫자 100만 개 선형 검색 및 이진 검색 비교
digit_list = [i for i in range(1, 1000000)]
test_n_small = 30
t1 = benchmark(lambda: linear_contains(digit_list, 900000), repeat=1)
print(f"linear_contains({test_n_small}) 1회 평균: {t1 * 1000:.6f} ms")
t2 = benchmark(lambda: binary_contains(digit_list, 900000), repeat=1)
print(f"binary_contains({test_n_small}) 1회 평균: {t2 * 1000:.6f} ms")
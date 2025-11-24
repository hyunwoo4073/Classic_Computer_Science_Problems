from enum import IntEnum
from typing import Tuple, List

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

# 파이썬 표준 라이브러리 bisect 모듈을 사용하여 이진 검색 가능
my_sorted_gene: Gene = sorted(my_gene)
print(binary_contains(my_sorted_gene, acg))
print(binary_contains(my_sorted_gene, gat))
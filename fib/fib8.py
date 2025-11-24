from functools import lru_cache
from typing import List, Tuple, Callable
import time


def fib7(n: int) -> int:
    """반복문 기반 피보나치 (O(n), O(1) 메모리)"""
    n1 = 0
    n2 = 1

    if n == 0 or n == 1:
        return n

    for _ in range(2, n + 1):
        current = n1 + n2
        n1 = n2
        n2 = current
    return current


# 메모이제이션 데코레이터
@lru_cache(maxsize=None)
def fib4(n: int) -> int:
    """재귀 + lru_cache 기반 피보나치 (논리상 O(n), 캐시 덕에 매우 빠름)"""
    if n < 2:
        return n
    return fib4(n - 2) + fib4(n - 1)


def check_correctness(max_n: int = 50) -> None:
    """0 ~ max_n까지 두 구현이 모두 같은 결과를 내는지 확인"""
    print(f"[정확성 검사] 0 ~ {max_n}까지 비교")
    for n in range(max_n + 1):
        a = fib7(n)
        b = fib4(n)
        if a != b:
            print(f"❌ 불일치: n={n}, fib7={a}, fib4={b}")
            return
    print("✅ 모든 n에서 fib7과 fib4 결과가 동일합니다.")


def benchmark(func: Callable[[int], int], n: int, repeat: int = 1) -> float:
    """주어진 함수(func)를 n에 대해 repeat번 호출했을 때 평균 실행 시간(초)을 리턴"""
    start = time.perf_counter()
    for _ in range(repeat):
        func(n)
    end = time.perf_counter()
    return (end - start) / repeat


if __name__ == "__main__":
    # 1. 두 구현 기본 테스트
    print("fib7(5)  =", fib7(5))
    print("fib7(50) =", fib7(50))
    print("fib4(5)  =", fib4(5))
    print("fib4(50) =", fib4(50))

    # 2. 정확성 비교
    check_correctness(max_n=50)

    # 3. 성능 비교
    test_n_small = 30
    test_n_large = 500

    print("\n[성능 비교 - 작은 n 한 번 실행]")
    fib4.cache_clear()
    t1 = benchmark(fib7, test_n_small, repeat=1)
    fib4.cache_clear()
    t2 = benchmark(fib4, test_n_small, repeat=1)
    print(f"fib7({test_n_small}) 1회 평균: {t1 * 1000:.6f} ms")
    print(f"fib4({test_n_small}) 1회 평균: {t2 * 1000:.6f} ms")

    print("\n[성능 비교 - 큰 n 한 번 실행]")
    fib4.cache_clear()
    t3 = benchmark(fib7, test_n_large, repeat=1)
    fib4.cache_clear()
    t4 = benchmark(fib4, test_n_large, repeat=1)
    print(f"fib7({test_n_large}) 1회 평균: {t3 * 1000:.6f} ms")
    print(f"fib4({test_n_large}) 1회 평균: {t4 * 1000:.6f} ms")

    print("\n[성능 비교 - 캐시 효과 (fib4를 여러 번 호출)]")
    fib4.cache_clear()
    # 첫 호출(캐시 채우기)
    warmup = benchmark(fib4, test_n_large, repeat=1)
    # 캐시 된 상태에서 여러 번
    cached = benchmark(fib4, test_n_large, repeat=1000)
    print(f"fib4({test_n_large}) 첫 호출(캐시 없음): {warmup * 1000:.6f} ms")
    print(f"fib4({test_n_large}) 캐시 후 1000회 평균: {cached * 1000:.6f} ms")

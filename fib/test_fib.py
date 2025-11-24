import pytest
from fib7 import fib7 
from fib4 import fib4


@pytest.mark.parametrize("n", range(0, 51))
def test_fib_correctness(n):
    assert fib7(n) == fib4(n)


def test_fib_basic_cases():
    assert fib7(0) == 0
    assert fib7(1) == 1
    assert fib7(5) == 5


def test_large_value():
    assert fib7(50) == fib4(50)


def test_fib4_cache_effect():
    fib4.cache_clear()
    first = fib4(35)  # 캐시 없음
    second = fib4(35) # 캐시 있음
    assert second == 9227465
    # 두 번째 호출이 훨씬 빨라짐 → 논리 테스트라 시간 비교는 안함

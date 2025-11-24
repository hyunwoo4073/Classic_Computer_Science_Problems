# 인자가 커질수록 호출 트리가 기하급수적으로 커짐
# fib(50)과 같이 함수를 호출하면 실행을 다 못할 수 있음

def fib2(n: int) -> int:
    if n < 2: # 기저 조건
        return n
    return fib2(n-2) + fib2(n-1) # 재귀 조건

if __name__ == "__main__":
    print(fib2(5))
    print(fib2(10))
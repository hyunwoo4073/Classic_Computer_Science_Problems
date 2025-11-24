def fib7(n: int) -> int:
    n1 = 0
    n2 = 1

    if n == 0 or n == 1:
        return n

    for i in range(2, n+1):
        current = n1 + n2
        n1 = n2
        n2 = current
    return current


if __name__ == "__main__":
    print(fib7(5))
    print(fib7(50))
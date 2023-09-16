import math

def primeFactors(n):
    factors = []

    while n % 2 == 0:
        factors.append(2)
        n = n // 2

    for i in range(3, int(math.sqrt(n)) + 1, 2):
        while n % i == 0:
            factors.append(i)
            n = n // i

    if n > 1:
        factors.append(n)

    return factors

def isUgly(n):
    if n <= 0:
        return False

    constraint = [2, 3, 5]
    prime = primeFactors(n)

    for i in prime:
        if i not in constraint:
            return False

    return True


n = 14
r = isUgly(n)

print(r)

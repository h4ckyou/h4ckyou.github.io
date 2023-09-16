def getPrime(n):
    is_prime = [True] * (n + 1)
    is_prime[0] = is_prime[1] = False
    p = 2

    while p ** 2 <= n:
        if is_prime[p]:
            for i in range(p ** 2, n + 1, p):
                is_prime[i] = False
        p += 1

    primes = [i for i in range(2, n + 1) if is_prime[i]]
    return primes


def countPrimes(n):
    factors = getPrime(n)
    count = 0

    for i in factors:
        if i < n:
            count += 1

    return count

n = 10
r = countPrimes(n)

print(r)%

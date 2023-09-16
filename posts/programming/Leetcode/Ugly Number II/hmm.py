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

def isUgly(num):
    constraint = [2, 3, 5]
    overkill = list(range(1, 2500))
    primes = [1]
    hashset = set()
    
    for i in overkill:
        n = primeFactors(i)
        for j in n:
            if j not in constraint:
                pass
            else:
                primes.append(i)
            
    for k in primes:
        hashset.add(k)
    
    final = list(hashset)
    print(final[:num+5])
    return final[num-1]
        
n = 11
r = isUgly(n)

# print(r)

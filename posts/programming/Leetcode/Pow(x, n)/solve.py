def myPow(x, n):
    if n < 0:
        x = 1 / x
        n = -n

    r = 1.0
    product = x

    while n > 0:
        if n % 2 == 1:
            r *= product
        product *= product
        n //= 2

    return r


x = 2.0
y = 10
r = myPow(x, y)

print(r) 

def generateTheString(n):
    if n % 2 == 0:
        return 'a'+'b'*(n-1)
    else:
        return 'a'*n

n = 10
r = generateTheString(n)

print(r)

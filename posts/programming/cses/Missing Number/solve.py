def find(n2, n1):
    expected = (n1 * (n1 + 1)) // 2
    known = sum(int(i) for i in n2)
    missing = expected - known
    return missing

n1 = int(input())
n2 = input().split()

r = find(n2, n1)
print(r)

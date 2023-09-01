def algo(n):
    r = [n]
    try:
        while r[-1] != 1:
            if n % 2 == 0:
                n = n // 2
            else:
                n = (n * 3) + 1
            r.append(n)
    except Exception:
        pass

    return r

n = int(input())
sequence = algo(n)
print(" ".join(map(str, sequence)))

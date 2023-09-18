def alternateDigitSum(n):
    sp = [int(i) for i in str(n)]
    a = []

    for i in range(len(sp)):
        if i % 2 == 0:
            a.append(sp[i])    
        else:
            a.append(-sp[i])
        
    return sum(a)

n = 521
r = alternateDigitSum(n)

print(r)

def countEven(num):
    cnt = 0

    for i in range(1, num+1):
        a = [int(j) for j in list(str(i))]
        sm = 0
        for k in a:
            sm += k

        if sm % 2 == 0 and i <= num:
            cnt += 1
               
    return cnt


num = 30
r = countEven(num)

print(r)

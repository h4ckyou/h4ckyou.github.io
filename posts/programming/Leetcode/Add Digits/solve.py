def addDigits(num):
    while True:
        sum = 0
        n = [int(i) for i in str(num)]

        for i in range(len(n)):
            sum += n[i]

        if len(str(sum)) == 1:
            return sum

        else:
            num = sum
    
num = 22
r = addDigits(num)

print(r)

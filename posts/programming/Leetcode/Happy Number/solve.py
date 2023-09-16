def isHappy(n):
    n = str(n)
    digit = ['2', '3', '4', '5', '6', '8','9']
    happy = False

    if n == '1':
        happy = True
    
    else:
        while n not in digit:
            s = 0 
            for i in n:
                s += pow(int(i), 2)
            
            if s == 1:
                happy = True
                break

            else:
                n = str(s)

    return happyr

n = 19
r = isHappy(n)

print(r)

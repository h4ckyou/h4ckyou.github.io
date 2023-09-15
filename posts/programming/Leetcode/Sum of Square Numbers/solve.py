import math

def judgeSquareSum(c):
    if c < 0:
        return False
    
    a_range = int(math.sqrt(c))

    for a in range(a_range + 1):
        bSquare = c - a * a
        b = int(math.sqrt(bSquare))

        if b * b == bSquare:
            return True
        
    return False

c = 5
print(judgeSquareSum(c))

def isBadVersion(n):
    bad = list(range(50000, 30000, -1))

    if n in bad:
        return True
    else:
        return False

def check(mid):
    if isBadVersion(mid) == True:
        if mid-1 >= 0 and isBadVersion(mid-1) == True:
            return "left"
        else:
            return "found"
    
    elif isBadVersion(mid) == False:
        return "right"

def firstBadVersion(number):
    left, right = 0, number

    while left <= right:
        mid = left + (right-left) // 2
        
        r = check(mid)
        
        if r == "found":
            return mid

        elif r == "right":
            left = mid + 1
        
        elif r == "left":
            right = mid - 1

    return None

number = 100000
res = firstBadVersion(number)

print(res)

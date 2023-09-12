def binarySearch(num):
    left, right = 0, num
    ans = 0

    while left <= right:
        middle = left + (right - left) // 2
        square = middle * middle

        if square == num:
            ans = middle
            break

        elif square > num:
            right = middle - 1

        else:
            left = middle + 1
            ans = middle  
    return ans


def isPerfectSquare(num):
    sqrt = binarySearch(num)

    if sqrt * sqrt == num:
        return True
    
    return False

num = 121
r = isPerfectSquare(num)

print(r)

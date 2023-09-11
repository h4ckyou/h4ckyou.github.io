def sqrt(num):
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

num = int(input())
result = sqrt(num)
print(result)

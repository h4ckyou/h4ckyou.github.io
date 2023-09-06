def isPalindrome(number):
    input = str(number)
    left, right = 0, len(input) - 1

    while left <= right:
        if input[left] != input[right]:
            return False

        left += 1
        right -= 1    

    return True

x = int(input())
r = isPalindrome(x)

print(r)

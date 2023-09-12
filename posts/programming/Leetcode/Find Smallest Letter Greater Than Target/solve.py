def nextGreatestLetter(letters, target):
    r = letters[0]

    left, right = 0, len(letters)-1

    while left <= right:
        mid = left + (right - left) // 2

        if letters[mid] > target:
            r = letters[mid]
            right = mid - 1
        else:
            left = mid + 1
    
    return r


letters = ["x","x","y","y"]
target = "z"

r = nextGreatestLetter(letters, target)
print(r)

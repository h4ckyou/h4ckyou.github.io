def binarySearch(array):
    left, right = 0, len(array) - 1

    while left < right:
        mid = left + (right - left) // 2

        if mid % 2 == 1:
            mid -= 1

        if array[mid] != array[mid + 1]:
            right = mid           
        else:
            left = mid + 2

    return array[left]

def singleNonDuplicate(nums):
    r = binarySearch(nums)

    return r


nums = [1, 1, 2]
r = singleNonDuplicate(nums)

print(r)

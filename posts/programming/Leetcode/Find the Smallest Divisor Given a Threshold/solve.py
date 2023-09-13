from math import ceil

def condition(array, divisor, threshold):
    val = sum([ceil(i / divisor) for i in array])

    return val <= threshold


def binarySearch(array, threshold):
    left, right = 1, max(array) * threshold

    while left < right:
        mid = left + (right - left) // 2
        r = condition(array, mid, threshold)

        if r:
            right = mid
        
        else:
            left = mid + 1
    
    return left
        


def smallestDivisor(nums, threshold):
    array = sorted(nums)
    r = binarySearch(array, threshold)

    return r

nums = [21212,10101,12121]
threshold = 1000000

r = smallestDivisor(nums, threshold)
print(r)

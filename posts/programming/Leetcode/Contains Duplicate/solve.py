def binarySearch(array, target):
    left, right = 0, len(array)-1

    while left <= right:
        mid = left + (right-left) // 2

        if array[mid] >= target:
            return True
        
        elif array[mid] < target:
            left = mid + 1
    
def containsDuplicate(nums):
    counter = {}

    for i in nums:
        if i in counter:
            counter[i] += 1
        else:
            counter[i] = 1
    
    array = sorted(list(counter.values()))
    if binarySearch(array, 2):
        return True

    return False
    
nums = [1,2,3,1]
r = containsDuplicate(nums)

print(r)

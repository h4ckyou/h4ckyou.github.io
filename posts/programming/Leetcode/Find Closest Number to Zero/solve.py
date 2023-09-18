def findClosestNumber(nums):
    array = sorted(nums)
    
    if array[0] >= 0:
        return array[0]
    
    elif array[-1] <= 0:
        return array[-1]
    
    j = float('inf')

    for num in nums:
        if abs(j) >= abs(num):
            if abs(j) == abs(num):
                if num > j:
                    j = num
            else:
                j = num

    return j

nums = [-10000, -10000, 10000, 10000]
r = findClosestNumber(nums) 

print(r)

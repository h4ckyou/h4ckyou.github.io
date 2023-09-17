def findMaxConsecutiveOnes(nums):
    if 0 not in nums:
        return len(nums)
    
    arr = []
    ptr = 0

    for i in range(len(nums)):
        arr.append(nums[i])
        
        if nums[i] == 0:
            arr.pop()
            ptr = max(ptr, len(arr))
            arr.clear()        
        else:
            ptr = max(ptr, len(arr))

    return ptr

nums = [1,0,1,1,0,1]
r = findMaxConsecutiveOnes(nums)

print(r)

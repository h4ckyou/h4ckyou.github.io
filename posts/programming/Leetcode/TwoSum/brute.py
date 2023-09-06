def brute(nums, target):
    for i in range(len(nums)):
        for j in range(i+1, len(nums)):
            if nums[i] + nums[j] == target:
                return [i, j]
        
    return None


nums = [3,2,4]
target = 6

result = brute(nums, target)
print(result)

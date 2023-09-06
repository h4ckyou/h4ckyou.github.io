def twoSum(nums, target):
    hashtable = {}

    for i, j in enumerate(nums):
        complement = target - j

        if complement in hashtable:
            return [hashtable[complement], i]

        hashtable[j] = i
    
    return None
            
nums = [2,7,11,15]
target = 9

result = twoSum(nums, target)
print(result)

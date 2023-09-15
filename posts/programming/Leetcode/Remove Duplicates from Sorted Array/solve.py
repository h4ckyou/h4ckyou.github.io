def removeDuplicates(nums):
    replace = 1
    for i in range(1, len(nums)):
        if nums[i] != nums[i-1]:
            nums[replace] = nums[i]
            replace +=1 
    
    return replace
    
nums = [1,1,2]
expectedNums = [1, 2]

k = removeDuplicates(nums)

assert k == len(expectedNums)
for i in range(k):
    assert nums[i] == expectedNums[i]
    print("True")

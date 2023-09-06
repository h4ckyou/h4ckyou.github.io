def twoSum(nums, target):
    array = sorted(nums)
    left, right = 0, len(array) - 1
    result = []

    while left <= right:
        sum = array[left] + array[right]

        if sum == target:
            result.append(nums.index(array[left]))
            result.append(nums.index(array[right]))
            return result

        elif sum > target:
            right -= 1
        
        else:
            left += 1

    return None
            
nums = [3,2,1,4]
target = 6

result = twoSum(nums, target)
print(result)

def shiftZeros(arr, n):
    unique = [num for num in arr if num != 0]
    zeros = [0] * (n - len(unique))
    
    return unique + zeros

def applyOperations(nums):
    for i in range(len(nums)-1):
        if nums[i] == nums[i+1]:
            nums[i] *= 2
            nums[i+1] = 0 
    
    r = shiftZeros(nums, len(nums))

    return r

nums = [847,847,0,0,0,399,416,416,879,879,206,206,206,272]
r = applyOperations(nums)

print(r)

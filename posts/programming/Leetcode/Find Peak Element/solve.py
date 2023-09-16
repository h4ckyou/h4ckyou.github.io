def findPeak(nums):
    left, right = 0, len(nums)-1
    # print([left, right])
    while left < right:
        mid = left + (right - left) // 2

        if nums[mid] < nums[mid+1]:
            left += 1
        
        elif nums[mid] > nums[mid+1]:
            right = mid

    return left 

def findPeakElement(nums):
    r = findPeak(nums)
    
    return r


nums = [1,2,3,1]
r = findPeakElement(nums)

print(r)

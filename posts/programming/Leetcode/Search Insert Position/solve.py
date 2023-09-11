def binarySearch(nums, target):
    left, right = 0, len(nums)-1
    while left <= right:
        mid = left + (right-left) // 2

        if nums[mid] == target:
            return mid
        
        elif nums[mid] > target:
            right = mid - 1

        elif nums[mid] < target:
            left = mid + 1

    return left

nums = [1,3,5,6]
target = 2

r = binarySearch(nums, target)
print(r)

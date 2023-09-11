def condition1(nums, target, mid):
    if nums[mid] == target:
        if mid-1 >= 0 and nums[mid-1] == target:
            return "left"
        else:
            return "found"
    
    elif nums[mid] > target:
        return "left"
    
    elif nums[mid] < target:
        return "right"
    

def condition2(nums, target, mid):
    if nums[mid] == target:
        if mid+1 <= len(nums)-1 and nums[mid+1] == target:
            return "right"
        else:
            return "found"
    
    elif nums[mid] > target:
        return "left"

    elif nums[mid] < target:
        return "right"


def getFirstPosition(nums, target):
    left, right = 0, len(nums)-1

    while left <= right:
        mid = left + (right-left) // 2
        r = condition1(nums, target, mid)

        if r == "found":
            return mid

        elif r == "left":
            right = mid - 1

        elif r == "right":
            left = mid + 1
        
    return -1

def getLastPosition(nums, target):
    left, right = 0, len(nums)-1

    while left <= right:
        mid = left + (right-left) // 2  
        r = condition2(nums, target, mid)

        if r == "found":
            return mid

        elif r == "left":
            right = mid - 1
        
        elif r == "right":
            left = mid + 1
        
    return -1

def searchRange(nums, target):
    return [getFirstPosition(nums, target), getLastPosition(nums, target)]

nums = [5,7,7,8,8,10]
target = 8

r = searchRange(nums, target)
print(r)

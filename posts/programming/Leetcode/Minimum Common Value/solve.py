def getLowerSize(nums1, nums2):
    array1 = []
    array2 = []

    if len(nums1) > len(nums2):
        array1 = nums2
        array2 = nums1
    elif len(nums1) == len(nums2):
        array1 = nums1
        array2 = nums2
    elif len(nums1) < len(nums2):
        array1 = nums1
        array2 = nums2
    
    return array1, array2

def binarySearch(array, target):
    left, right = 0, len(array)-1

    while left <= right:
        mid = left + (right-left) // 2

        if array[mid] == target:
            return True
        
        elif array[mid] > target:
            right = mid - 1
        
        elif array[mid] < target:
            left = mid + 1
        
    return False

def getCommon(nums1, nums2):
    array1, array2 = getLowerSize(nums1, nums2)

    for i in array1:
        if binarySearch(array2, i):
            return i
        
    return -1

nums1 = [2,4]
nums2 = [1,2]

r = getCommon(nums1, nums2)
print(r)


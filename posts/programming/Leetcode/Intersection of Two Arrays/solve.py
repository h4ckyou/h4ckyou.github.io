def binarySearch(array, target):
    left, right = 0, len(array)-1

    while left <= right:
        mid = left + (right-left) // 2
        
        if array[mid] == target:
            return array[mid]
        
        elif array[mid] > target:
            right = mid - 1

        elif array[mid] < target:
            left = mid + 1
   
    return -1
    
def removeDuplicate(result):
    dup = []
    
    for i in range(len(result)):
        if i == 0 or result[i] != result[i - 1]:
            dup.append(result[i])
    
    return dup
    
def intersection(num1, num2):
    array = sorted(num1)
    check = sorted(num2)
    result = []
    final = []

    # Get the intersect values from each array
    for target in check:
        r = binarySearch(array, target)
        if r != -1:
            result.append(r)
    
    # Sort result array to help remove duplicates
    result = sorted(result)

    if len(result) == 1:
        return result

    final = removeDuplicate(result)
            
    return final


nums1 = [54,93,21,73,84,60,18,62,59,89,83,89,25,39,41,55,78,27,65,82,94,61,12,38,76,5,35,6,51,48,61,0,47,60,84,9,13,28,38,21,55,37,4,67,64,86,45,33,41]
nums2 = [17,17,87,98,18,53,2,69,74,73,20,85,59,89,84,91,84,34,44,48,20,42,68,84,8,54,66,62,69,52,67,27,87,49,92,14,92,53,22,90,60,14,8,71,0,61,94,1,22,84,10,55,55,60,98,76,27,35,84,28,4,2,9,44,86,12,17,89,35,68,17,41,21,65,59,86,42,53,0,33,80,20]

r = intersection(nums1, nums2)
print(r)

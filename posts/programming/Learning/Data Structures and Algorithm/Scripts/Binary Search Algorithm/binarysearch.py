# Iterative Binary Search Algorithm

def binarySearch(array, target):
    if len(array) == 0:
        return -1

    left, right = 0, len(array)-1

    while left <= right:
        
        middle = left + (right - left) // 2

        if array[middle] == target:
            return middle

        elif array[middle] < target:
            left = middle + 1

        else:
            right = middle - 1
        
    return -1

array = [-1,0,3,5,9,12]
target = 9

result = binarySearch(array, target)
print(result)

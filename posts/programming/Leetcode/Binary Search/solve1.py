# Iterative Binary Search Algorithm

def binarySearch(arr, x):
    l = 0
    r = len(arr)-1

    while l <= r:
        
        mid = l + (r - l) // 2

        if arr[mid] == x:
            return mid

        elif arr[mid] < x:
            l = mid + 1

        else:
            r = mid - 1
        
    return -1


arr = [-1,0,3,5,9,12]
x = 9

result = binarySearch(arr, x)
print(result)

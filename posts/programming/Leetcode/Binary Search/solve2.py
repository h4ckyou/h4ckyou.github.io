# Recursive Binary Search Algorithm

def binarySearch(arr, x, l, r):
    mid = l + (r-l)//2

    while r >= 0:

        if arr[mid] == x:
            return mid
        
        elif arr[mid] < x:
            return binarySearch(arr, x, l+1, r)
        
        else:
            return binarySearch(arr, x, l, mid-1)


arr = [-1,0,3,5,9,12]
x = 9
l = 0
r = len(arr)-1

result = binarySearch(arr, x, l, r)
print(result)

# Linear Search Algorithm

def search(arr, N, k):
    idx = 1
    position = 0

    for i in range(1, N+1):
        if arr[i - idx] == k:
            position = i
            break
        else:
            position = -1
    
    return position

arr = [9, 7, 2, 16, 4, 5, 1, 3, 10, 25, 31, 45, 60, 200]
N = len(arr)
k = 16

res = search(arr, N, k)
print(res)

def findKthPositive(arr, k):
    count = 0
    number = 1

    while True:
        if number not in arr:
            count += 1
        
        if count == k:
                return number
        
        number += 1


arr = [2,3,4,7,11]
k = 5

r = findKthPositive(arr, k)
print(r)

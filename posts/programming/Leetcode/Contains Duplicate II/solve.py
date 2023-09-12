def containsNearbyDuplicate(nums, k):
    hashtable = {}

    for i, num in enumerate(nums):
        if num in hashtable and abs(i - hashtable[num]) <= k:
            return True
        hashtable[num] = i

    return False

nums = [1,0,1,1]
k = 1
result = containsNearbyDuplicate(nums, k)
print(result) 

def majorityElement(nums):
    hashtable = {}
    condition = len(nums)//2

    for num in nums:
        if num in hashtable:
            hashtable[num] += 1
        else:
            hashtable[num] = 1
    
    idx = list(hashtable.values())

    if max(idx) > condition:
        for key, value in hashtable.items():
            if value == max(idx):
                return key
        
    return -1


nums = [2,2,1,1,1,2,2]
r = majorityElement(nums)

print(r)

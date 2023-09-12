def majorityElement(nums):
    hashtable = {}
    condition = len(nums)//3
    r = []

    for num in nums:
        if num in hashtable:
            hashtable[num] += 1
        else:
            hashtable[num] = 1
    

    for key, value in hashtable.items():
        if value > condition:
            r.append(key)

    return r


nums = [1, 2]
r = majorityElement(nums)

print(r)

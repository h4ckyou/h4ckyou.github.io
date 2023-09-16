def findDuplicate(nums):
    count = {}

    for i in nums:
        if i in count:
            count[i] += 1
        else:
            count[i] = 1
    #print(count)
    for key, value in count.items():
        if value >= 2:
            return key
    


nums = [2,2,2,2,2]
r = findDuplicate(nums)

print(r)

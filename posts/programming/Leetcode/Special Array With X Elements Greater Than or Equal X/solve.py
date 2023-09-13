def specialArray(nums):
    x = 1

    while x <= len(nums):
        count = 0

        for num in nums:
            if num >= x:
                count += 1
    
        if count == x:
            return x

        x += 1
        
    return -1

nums = [0,4,3,0,4]
r = specialArray(nums)

print(r)

def intersection(nums1, nums2):
    result = []

    count = {}
    for num in nums1:
        if num in count:
            count[num] += 1
        else:
            count[num] = 1

    for num in nums2:
        if num in count and count[num] > 0:
            result.append(num)
            count[num] -= 1
    
    return result

nums1 = [4,9,5]
nums2 = [9,4,9,8,4]

r = intersection(nums1, nums2)
print(r)

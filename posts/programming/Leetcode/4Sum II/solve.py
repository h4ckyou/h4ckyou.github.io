def fourSumCount(nums1, nums2, nums3, nums4):
    n = len(nums1)
    count = 0 

    hashtable = {}

    for i in range(n):
        for j in range(n):
            sum1 = nums1[i] + nums2[j]
           
            if sum1 in hashtable:
                hashtable[sum1] += 1
            else:
                hashtable[sum1] = 1

    for i in range(n):
        for j in range(n):
            sum2 = nums3[i] + nums4[j]
            target = -sum2

            if target in hashtable:
                count += hashtable[target]

    return count

nums1, nums2, nums3, nums4 = [1, 2], [-2, -1], [-1, 2], [0, 2]
r = fourSumCount(nums1, nums2, nums3, nums4)
print(r)

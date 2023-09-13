def fourSumCount(nums1, nums2, nums3, nums4):
    n, hashtable, count = len(nums1), {}, 0

    for i in range(n):
        for j in range(n):
            sum = nums1[i] + nums2[j]

            if sum in hashtable:
                hashtable[sum] += 1
            else:
                hashtable[sum] = 1
    
    for k in range(n):
        for l in range(n):
            check = 0 - (nums3[k] + nums4[l])
            
            if check in hashtable:
                count += hashtable[check]

    return count

nums1, nums2, nums3, nums4 = [1, 2], [-2, -1], [-1, 2], [0, 2]
r = fourSumCount(nums1, nums2, nums3, nums4)
print(r)

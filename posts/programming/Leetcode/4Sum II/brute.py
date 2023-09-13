def fourSumCount(nums1, nums2, nums3, nums4):
    n = len(nums1)
    count = 0 

    for i in range(n):
        for j in range(n):
            for k in range(n):
                for l in range(n):
                    sum = nums1[i] + nums2[j] + nums3[k] + nums4[l]

                    if sum == 0:
                        count += 1

    return count

nums1, nums2, nums3, nums4 = [1, 2], [-2, -1], [-1, 2], [0, 2]
r = fourSumCount(nums1, nums2, nums3, nums4)
print(r)

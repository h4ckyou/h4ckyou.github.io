def merge(nums1, nums2, m, n):
    position = m + n - 1
    i, j = m - 1, n - 1

    while i >= 0 and j >= 0:
        if nums1[i] >= nums2[j]:
            nums1[position] = nums1[i]
            i -= 1
        else:
            nums1[position] = nums2[j]
            j -= 1
        position -= 1

    while j >= 0:
        nums1[position] = nums2[j]
        j -= 1
        position -= 1

    return nums1

nums1 = [1,2,3,0,0,0]
m = 3
nums2 = [2,5,6]
n = 3

r = merge(nums1, nums2, m, n)
print(r)


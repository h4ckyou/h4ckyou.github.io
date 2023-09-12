def getMaxDigits(nums):
    hashtable = {}

    for i in range(len(nums)):
        for j in range(i+1, len(nums)):
            # print([nums[i], nums[j]])
            a, b = max([int(k) for k in list(str(nums[i]))]), max([int(m) for m in list(str(nums[j]))])
            if a == b:
                sum = nums[i] + nums[j]
                hashtable[sum] = sum

    return hashtable

def maxSum(nums):
    digits = getMaxDigits(nums)

    # Incase no value found
    if len(digits) == 0:
        return -1

    maximum = max(list(digits.values()))

    return maximum

nums = [84,91,18,59,27,9,81,33,17,58]
r = maxSum(nums)

print(r)

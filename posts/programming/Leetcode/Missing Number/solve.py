def findMissingNumber(nums):
    maximum = len(nums)
    expected = (maximum * (maximum + 1)) // 2
    known = sum(nums)
    missing = expected - known

    return missing


nums = [9,6,4,2,3,5,7,0,1]
r = findMissingNumber(nums)

print(r)

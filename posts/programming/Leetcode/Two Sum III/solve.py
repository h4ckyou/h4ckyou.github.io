def binarySearch(array):
    result = []

    for i in range(len(array) - 2):
        if i > 0 and array[i] == array[i - 1]:
            continue

        left, right = i + 1, len(array) - 1

        while left < right:
            sum = array[i] + array[left] + array[right]

            if sum == 0:
                result.append([array[i], array[left], array[right]])

                while left < right and array[left] == array[left + 1]:
                    left += 1
                while left < right and array[right] == array[right - 1]:
                    right -= 1

                left += 1
                right -= 1

            elif sum < 0:
                left += 1

            else:
                right -= 1
    
    return result

def threeSum(nums):
    array = sorted(nums)
    result = binarySearch(array)

    return result

nums = [-1,0,1,2,-1,-4]
r = threeSum(nums)

print(r)

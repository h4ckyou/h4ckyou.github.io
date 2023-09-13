def binarySearch(array, target):
    result = []
    
    for j in range(len(array) - 3):
        for i in range(j+1, len(array) - 2):                       
            left, right = i + 1, len(array) - 1

            # print([j, i])

            while left < right:
                sum = array[j] + array[i] + array[left] + array[right]

                # print("Position")
                # print([j, i, left, right])
                # print("Values")
                # print([array[j], array[i], array[left], array[right]])

                if sum == target:
                    result.append([array[j], array[i], array[left], array[right]])
                    left += 1
                    right -= 1

                elif sum < target:
                    left += 1

                else:
                    right -= 1
    
    return result

def fourSum(nums, target):
    array = sorted(nums)
    result = binarySearch(array, target)
    hashmap = set()

    for mat in result:
        hashmap.add(tuple(mat))

    return [list(i) for i in hashmap]

nums = [1,0,-1,0,-2,2]
target = 0

r = fourSum(nums, target)
print(r)

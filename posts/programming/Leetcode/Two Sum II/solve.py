def twoSum(array, target):
    hashtable = {}

    for i, num in enumerate(array):
        complement = target - num

        if complement in hashtable:
            return ([hashtable[complement]+1, i+1])
        else:
            hashtable[num] = i
            
numbers = [-1,0]
target = -1

r = twoSum(numbers, target)
print(r)

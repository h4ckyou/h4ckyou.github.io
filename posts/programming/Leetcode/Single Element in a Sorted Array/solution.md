<h3> Single Element in a Sorted Array </h3>

![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/3102f722-59e9-4b13-b6f5-36de965430e5)

# Approach

Looking at the problem we can tell we'll be given an array `nums` and we're too basically find that element in the array which only appears once

A good way to start is to try solve this using a brute force approach as it helps to confirm if there's a solution to this problem

And basically my brute force approach would use Linear Search which basically does this:
- Iterate through the array and if `array[i] != array[i-1]` and `array[i] != array[i+1]` that means the non duplicate value is `array[i]`
- There are cases we should check like if `len(array) == 1` then we return `array[0]` because there's only one element in the array or if the first element isn't equal to the second i.e `array[0] != array[1]` 
- If we have exhaused our loop then the result is the last element of the array

Here's the implementation:

```python
def singleNonDuplicate(array):

    if len(array) == 1:
        return array[0]

    if array[0] != array[1]:
        return array[0]

    for i in range(1, len(array)-1):
        if array[i] != array[i-1] and array[i] != array[i+1]:
            return array[i]

    return array[-1]

nums = [1,1,2,3,3,4,4,8,8]
r = singleNonDuplicate(nums)

print(r)
```

That works but the problem with it is the complexity:

```
Time Complexity: O(N)
Space Complexity: O(1)
```

So now we can optimize the program

The way I'll do it is using Binary Search

Here's the explanation:
- I initialized two pointers, `left` and `right`, to the first and last index of the array, respectively.
- I'll use a while loop which will keep on running as long as `left` is less than `right`.
- I then will calculate the middle index `mid` using the formular for binary search. I will need to make sure that the value of `mid` is always an even number so as to keep it consistent with the pairs of elements we want to compare with
- Now I compare the element at `mid` with `mid+1`. If they are not equal it means the non-duplicate element is to the left side of the array. So I update the `right` value to the mid so as to narrow the search range to half left of the array
- If the element at `mid` and `mid+1` is equal that means the non-duplicate value is at the right side of the array. If so I'll update `left` to `mid+2` instead of `mid+1` because I have already checked the pair of elements at `mid` and `mid+1` and we would want to move to the next pair of element
- I''ll continue this loop till `left` is no longer less than `right`. At this point the value of `left` will be pointing to the single non-duplicate value which we can then return 

# Complexity
- Time complexity:

```
O(log n)
```

- Space complexity:

```
O(1)
```

Solve Script: [link](https://github.com/h4ckyou/h4ckyou.github.io/blob/main/posts/programming/Leetcode/Single%20Element%20in%20a%20Sorted%20Array/solve.py)

It works!
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/f9b573f8-235d-457c-8e9a-83e6244d4d2b)

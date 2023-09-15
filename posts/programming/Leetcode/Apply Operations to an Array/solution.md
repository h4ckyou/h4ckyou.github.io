<h3> Apply Operations to an Array </h3>

![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/da7d5c18-bbb1-464b-a271-d59539579bdf)
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/7ca8c74b-0924-4347-b5cd-9def719490a2)

We are going to be given an array `nums` of size `n` containing non-negative integers

We may apply `n-1` operations to this array where, in the `ith` operation (0-indexed), you will apply the following on the `ith` element of nums:
- If `nums[i] == nums[i + 1]`, then multiply `nums[i]` by `2` and set `nums[i + 1]` to `0`. Otherwise, you skip this operation.

After performing all the operations, shift all the `0's` to the end of the array.

Let's take an example:

Consider this array:

```
nums = [1,2,2,1,1,0]
```

First there are 6 elements in this array and we can perform 5 operations on it.

We'll first iterate through the elements in this array and check this condition

For the first iteration which will start from index 0 we'll check this:

```
nums[0] == nums[1]
```

Basically that will compare the vale of `1 and 2` together since they are not equal we won't apply the operation on it

The second iteration will check this:

```
nums[1] == nums[2]
```

Which translates to `2 == 2`, in this case it is True so now for the operation we do this:

```
nums[1] = nums[1] * 2
nums[2] = 0
```

So the value stored in those index will then be `4 and 0`

We'll move to the next iteration

```
nums[2] == nums[3]
```

Rememer that we've set `nums[2]` to `0` so we're comparing `0 and 1` since it isn't equal we skip the operation

```
nums[3] == nums[4]
```

In this case the comparison is true because `1 == 1` and now we apply the operation

```
nums[3] = nums[3] * 2
nums[4] = 0
```

The last iterate is this:

```
nums[4] == nums[5]
```

It returns true because `0 == 0` and the operation would also evaluate to `0` for both elements

The final result after all this operation has been done is:

```
[1, 4, 0, 2, 0, 0]
```

The next thing would be the return value is the elements in the array with the zero's shifted to the right

So it's this:

```
[1, 4, 2, 0, 0, 0]
```

The first case which is to calculate if the operation can be done is easy to do as we can just iterate through each elements in the array and check for the condition


As for the shifting of the zero the way I approached it is by creating an array containing all the elements of the resulting operation whose value is not zero

Then I filled another array containing the amount of zero from the resulting operation and this is calculated from `(len(nums) - len(unique))`

With that we would have two arrays containing the non zero elements and the zero element which we can just concatenate together

Here's my solve script: [link](https://github.com/h4ckyou/h4ckyou.github.io/blob/main/posts/programming/Leetcode/Apply%20Operations%20to%20an%20Array/solve.py)
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/0720cf5d-6542-4dce-b581-d467c459c62e)


#### Leetcode Submission Script

```python
def shiftZeros(arr, n):
    unique = [i for i in arr if i != 0]
    zero = [0] * (n - len(unique))

    return unique + zero

class Solution:
    def applyOperations(self, nums: List[int]) -> List[int]:
        for i in range(1, len(nums)):
            if nums[i-1] == nums[i]:
                nums[i-1] *= 2
                nums[i] = 0 
        
        r = shiftZeros(nums, len(nums))

        return r
```



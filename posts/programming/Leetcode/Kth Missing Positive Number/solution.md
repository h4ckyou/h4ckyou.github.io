<h3> Kth Missing Positive Number </h3>

![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/4dbc6d56-931c-4485-8f1e-265b6ea8af02)

We are given an array which is sorted in increasing order with an integer `k`

Our goal is to return the `Kth` positive integer that's missing from the array

#### Approach

One way we can easily solve this is:

First we can store a list of possible values within a specific range in this case I used `5001` in an array `possible[]`

Now I can iterate through each values in the `possible[i]` and see if the iterate isn't among the `array[j]`

Is that returns True I'll save those elements in another array `missing` then return the `kth` missing value which we can represent as `missing[k]`

That said it's pretty simple but the issue is what if our `kth` value is more than the value in `possible` that would return an error!

Also it's efficiency is bad
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/8a75efa6-48a9-4b05-b031-326b88cb4949)

It uses much space and time because we're storing a large value in memory and iterating through a large array

So let's optmize that!

Instead of using lot of memory we can optimize that 

I'll keep the current number not in the array in a variable and keep track of when we get the `k` which would be possible if I make a variable `count` that increments on each check of `currentNumber`
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/9b854c11-952a-48a7-af69-048012c3c34a)

In terms of space complexity I improved it but in terms of time I didn't :(

Solve Script: [link](https://github.com/h4ckyou/h4ckyou.github.io/blob/main/posts/programming/Leetcode/Kth%20Missing%20Positive%20Number/solve.py)

After looking at other people solution I found this one which implemented Binary Search

Here's how it's done: 
- We initialize the two pointers `left` and `right` to narrow down the search range then we get the middle element `mid`
- Now we need to calculate the number of missing elements before `arr[mid]` which can be gotten using this equation `arr[mid] - (mid + 1)`
- If the value is less than `k` that means the `Kth` missing number is on the right hand side which we'll then increment `left` to `mid + 1`
- Else that means the `Kth` missing number is on the left hand side and we can then shift our search space to the left using `right = mid - 1`
- At the end of the loop, `left` will be pointing to the index where the `Kth` missing number would be inserted.
- We know that there are `missing_before_mid` missing numbers before `arr[mid]`, so the `Kth` missing number would be `arr[mid] + (k - missing_before_mid)`.
- Then we return `left + k`

Script:

```python
def findKthPositive(arr, k):
    left, right = 0, len(arr)-1

    while left <= right:
        mid = left + (right - left) // 2

        missing = arr[mid] - (mid + 1)

        if missing < k:
            left = mid + 1
        
        else:
            right = mid - 1
        
    # arr[mid] + (k - missing) == kth missing number
    return left + k

arr = [2,3,4,7,11]
k = 5

r = findKthPositive(arr, k)
print(r)
```

Running it works and it's fast since the time complexity is `O(log N)`
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/4552bd05-d90f-4313-96ff-381a7a3cc69c)



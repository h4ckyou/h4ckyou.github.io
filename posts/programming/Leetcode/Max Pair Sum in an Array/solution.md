<h3> Max Pair Sum in an Array </h3>

![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/2a791492-1663-4350-bb9d-d02a80d1a457)

When I was trying to solve this what I thought was the meaning of `maximum digit in both numbers are equal.` was wrong which eventually lead to failed case
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/8b4747ea-2ef3-482d-8976-1b9a611076c0)

Here is the thought process for that:

1. We are given an array `nums` which holds integer values starting from index 0
2. We are to find the maximum sum of pair of numbers from the array `nums`, such that the maximum digit in both numbers are equal
3. So let's say I have this array `[12, 21, 15, 51]`, the list of sum of digits in the array is `{3, 6}` which is formed from `[1+2 == 2+1]` and `[1+5 == 5+1]` respectively
4. Now we need to maximum pair of the list of sum of digits from the array which in this case is 66 because `51+15 > 12 + 21`
5. My solution will involve getting all values such that the digit in both numbers are equal which will be stored in a hashtable
6. Then I'll get the maximum value from the hashtable

Then I wrote the script:

```python
def getMaxDigits(nums):
    hashtable = {}

    for i in range(len(nums)):
        for j in range(i+1, len(nums)):
            a, b = nums[i], int(str(nums[j])[::-1])
            if a == b:
                val = [int(i) for i in list(str(a))]
                sum = 0
                for i in range(len( val)):
                    sum += val[i]

                hashtable[a] = sum
    
    return hashtable

def maxSum(nums):
    digits = getMaxDigits(nums)

    # Incase no value found
    if len(digits) == 0:
        return -1
        
    maximum = max(list(digits.values()))

    for key, value in list(digits.items()):
        if value == maximum:
            pair = int(str(key)[::-1]) + key
            
            return pair
    
    return -1


nums = [1,2,3,4]
r = maxSum(nums)

print(r)
```

But it worked for some test case till I reached this `[31,25,72,79,74]` 

The expected output is `146` but my program is returning `-1` 

If you look at it based on my assumption made the return value is right but what's the issue?

Then I had to understand what the statement meant exactly and came up with another solution

So it means that we're to find the maximum sum of pair of numbers from the array `nums` such that the maximum digit in pair are equal

What that means is this:

Let's take this array for example `[15, 25, 1, 2]`

The maximum digit in the number is:

```
max(15) = 5
max(25) == 5
```

And the sum of the pair is `40`

Since there are no other numbers in the array that meets the condition therefore the result is `40`

Here's my final solve script: [link]()
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/6400b80a-f9c1-4666-aec4-ddd7d960216f)

It isn't too efficient :(

Here's a better approach I read from other people solution

Approach:

- Find max digit for each number in the array `nums`
- Store them in a hash map, group them with same `max_digit` into a list
- Sort and find the max two numbers for each `max_digit`

Complexity:

```
Time complexity: O(nlogn)
Space complexity: O(n)
```

Code:

```python
class Solution:
    def maxSum(self, nums: List[int]) -> int:
        d = defaultdict(list)
        ans = -1

        for each in nums:
            max_digit = int(max(str(each)))
            d[max_digit].append(each)

        for each in d:
            if len(d[each]) > 1:
                d[each].sort()
                ans = max(ans, d[each][-1] + d[each][-2])    
                
        return ans
```

You can see it's way faster 
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/deb4520c-3fb7-4880-8791-4309af829d40)


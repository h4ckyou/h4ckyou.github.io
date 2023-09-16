<h3> Longest Common Prefix </h3>

![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/f8b8a598-c2ec-408d-bf62-47d973ce762e)

Write a function to find the longest common prefix string amongst an array of strings.

If there is no common prefix, return an empty string "".

So let's say we have this array of string:

```
s = ["flower","flow","flight"]
```

We need to find the longest common prefix which means the longest string that occurs in all string of the array

In this case it's `fl` since it occurs in both `s[1] and s[2]`

One approach we can use is to Brute Force but that isn't an optimized way because it would take time since we'll be basically checking each character of the first element in the array with other elements in the array

So here's a more optimized solution

We can sort the array which would then arrange the elements in increasing order

With it being sorted that means the smallest value would be the first and the largest value would be the last

One important thing here is that due to it being sorted that means it will be sorted lexicographically meaning that it will be arranged in alphabetical order

This can help us limit the longest prefix because of this:
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/ce3f6842-cb6f-4db6-8a48-7a5afc9df175)

Instead of us searching the whole elements now we know that since it's sorted we will just search within the first and last element because any other element within it would be less than the last element and would have the same common prefix

So our comparison would be within the first and last element
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/ab379849-b1d4-4644-8321-03ee459004dc)

Here's my solve script: [link](https://github.com/h4ckyou/h4ckyou.github.io/blob/main/posts/programming/Leetcode/Longest%20Common%20Prefix/solve.py)
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/cc0f8509-9a95-4766-bf6d-d7aff8dacfc0)


#### Leetcode Submission Code

```python
class Solution:
    def longestCommonPrefix(self, strs: List[str]) -> str:
        array = sorted(strs)

        first = array[0]
        last = array[len(strs)-1]
        r = ""

        for i in range(len(first)):
            if first[i] != last[i]:
                break
            else:
                r += first[i]

        if len(r) != 0:
            return r
        else:
            return ""
```

<h3> Counting Words With a Given Prefix </h3>

![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/4c89ba6d-9994-490b-918d-236bac56e18a)

You are given an array of strings `words` and a string `pref`.

Return the number of strings in `words` that contain `pref` as a prefix.

A prefix of a string `s` is any leading contiguous substring of `s`.

My approach to solve this is to iterate through every elements in the array `words` then check if `words[:len(pref)] == pref`

If that is True then i increment the variable `count` by `1`

Here's my solve script: [link](https://github.com/h4ckyou/h4ckyou.github.io/blob/main/posts/programming/Leetcode/Counting%20Words%20With%20a%20Given%20Prefix/solve.py)
![win](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/9b592d99-4b27-447a-9706-8ea9ab63afca)

First time I'm getting 100% in space complexity....well I'm not really using any space :) making the space complexity `O(1)` which is constant i.e doesn't depend on the input size

While the time complexity is `O(N*M)` where `N` is the number of words in the `words` array and `M` is the length of the `pref`

#### Leetcode Submission Script

```python
class Solution:
    def prefixCount(self, words: List[str], pref: str) -> int:
        count = 0
        n = len(pref)

        for i in words:
            if i[:n] == pref:
                count += 1

        return count
```

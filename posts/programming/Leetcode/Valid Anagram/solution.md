<h3> Valid Anagram </h3>

![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/741598fc-f1d7-4e3b-8e1e-3ac7fb5b2e5f)

Given two strings `s` and `t`, return true if `t` is an anagram of `s`, and false otherwise.

An `Anagram` is a word or phrase formed by rearranging the letters of a different word or phrase, typically using all the original letters exactly once.

They are various ways we can solve this and one way is this:
- Get the occurrence of each character in both string and store in a hash table
- For each key and value pair in `htS`, I'll check if `htT[s] != value` if it isn't then I return False
- I'll also check if each key of `htT` is among `htS`  if it isn't then I return False
- And the last check is if the length of both string are not the same then I return False

Here's the solve script: [link](https://github.com/h4ckyou/h4ckyou.github.io/blob/main/posts/programming/Leetcode/Valid%20Anagram/solve.py)
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/53d40d60-d923-46bc-bc68-64159ab233f5)

Another way to easily solve this is to first sort both strings then check if they are the same or not

Since for it to be anagram each they basically need to be the same after arranging the letters if scattered

Here's the script:

```python
class Solution:
    def isAnagram(self, s: str, t: str) -> bool:
        if sorted(s) != sorted(t):
            return False
        
        return True
```
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/9af833ba-3f02-4aef-afee-217e5b66b508)

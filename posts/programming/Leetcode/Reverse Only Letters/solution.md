<h3> Reverse Only Letters </h3>

![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/909266b5-4a15-4a1c-ada7-076bc815ae82)

Given a string `s`, reverse the string according to the following rules:
- All the characters that are not English letters remain in the same position.
- All the English letters (lowercase or uppercase) should be reversed.

Return `s` after reversing it.

My approach is this:

- Initialize two pointers `left` and `right` which would hold the `0th` and last index `len(s)-1` value
- In a while loop I'll check:
    - To check for if the value of `s[left]` of the string is not `alpha()` I'll make a while loop that checks for that and I'll increment the left pointer by 1
    - To check for if the value of `s[right]` of the string is not `alpha()` I'll make a while loop that checks for that and I'll decrement the right pointer by 1
    - The point at which they exist two values where `s[left]` and `s[right]` is `alpha()` I'll then swap them i.e I'll set ``s[left], s[right] =  s[right], s[left]``
- Then I'll increment the left pointer by 1 and decrement the right pointer by 1 to keep the process going till I reach the condition where left > right then the loop finishes and I get a reversed string that meets the condition
   
Solve Script: [link](https://github.com/h4ckyou/h4ckyou.github.io/blob/main/posts/programming/Leetcode/Reverse%20Only%20Letters/solve.py)
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/697658ca-919d-41ca-a8c4-cf9db9db9dc8)


#### Leetcode Submission Script

```python
class Solution:
    def reverseOnlyLetters(self, s: str) -> str:
        s = list(s)

        left, right = 0, len(s)-1

        while left < right:

            while left < right and s[left].isalpha() == False:
                left += 1

            while left < right and s[right].isalpha() == False:
                right -= 1
            
            if s[left].isalpha() and s[right].isalpha():
                s[left], s[right] = s[right], s[left]

            
            left += 1
            right -= 1
        
        r = "".join(s)

        return r
```

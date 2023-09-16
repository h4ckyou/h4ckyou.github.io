<h3> Reverse Only Letters </h3>

![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/909266b5-4a15-4a1c-ada7-076bc815ae82)

Given a string `s`, reverse the string according to the following rules:
- All the characters that are not English letters remain in the same position.
- All the English letters (lowercase or uppercase) should be reversed.

Return `s` after reversing it.

My approach is to use two pointers `left` and `right` and check for those condition then swap the characters at the position of the two pointers if `s[left]` and `s[right]` are English letters

Solve Script: [link]()
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

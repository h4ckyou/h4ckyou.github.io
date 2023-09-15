<h3> Valid Parentheses </h3>

![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/a5671ea7-2308-4d1e-9a9a-67da775d43ce)

Given a string `s` containing just the characters `'(', ')', '{', '}', '[' and ']'`, determine if the input string is valid.

An input string is valid if:
- Open brackets must be closed by the same type of brackets.
- Open brackets must be closed in the correct order.
- Every close bracket has a corresponding open bracket of the same type.

From the question we know that we'll be given a string containing the symbols above

Our goal is to check if it's a valid parenthesis

One way to approach this is to use the Stack Data Structure

The idea basically is this:
- We'll push the opening parenthesis onto the stack if we find one
- Then when we encounter a closing parenthesis we pop the value from the stack and compare the mapping of the character in the hashtable if they are the same
- If they match we keep continuing the process till we traverse all characters in the string
- If after traversing we check if there's value on the stack and if the string is a valid parenthesis they won't be any value on the stack because it would have been popped out already
- So that's going to be our return boolean value

Here's my solve script: [link](https://github.com/h4ckyou/h4ckyou.github.io/blob/main/posts/programming/Leetcode/Valid%20Parentheses/solve.py)
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/642a26d9-26ae-454a-a394-d90494e54ff7)


#### Leetcode Submission Script

```python
class Solution:
    def isValid(self, s: str) -> bool:
        parenthesis = {')': '(', '}': '{', ']': '['}
        stack = []

        for char in s:
            if char in parenthesis.values():
                stack.append(char)
            
            elif char in parenthesis.keys():
                if not stack or stack.pop() != parenthesis[char]:
                    return False

        return len(stack) == 0
```

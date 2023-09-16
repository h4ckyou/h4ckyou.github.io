<h3> Faulty Keyboard </h3>

![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/b12813ac-2d63-49e2-b543-0d71ddd936b3)
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/04d9af92-79f8-4ec5-8a3f-d97b6cbaecfb)

Your laptop keyboard is faulty, and whenever you type a character `'i'` on it, it reverses the string that you have written. Typing other characters works as expected.

You are given a 0-indexed string `s`, and you type each character of `s` using your faulty keyboard.

Return the final string that will be present on your laptop screen.

So my approach to solve this is to iterate through each character in the string and append them to a new list during the iteration when I find the character `i` I'll remove the value of the last element in the list which would be `i` then reverse the list

My solve script is in the below link.

Solve Script: [link](https://github.com/h4ckyou/h4ckyou.github.io/blob/main/posts/programming/Leetcode/Faulty%20Keyboard/solve.py)
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/0373819e-2ca0-4b94-9ba9-094924f32a0d)


#### Leetcode Submission Script

```python
class Solution:
    def finalString(self, s: str) -> str:
        s = list(s)
        rev = []

        for i in range(len(s)):
            rev.append(s[i])
            if s[i] == 'i':
                rev.pop()
                rev = rev[::-1]        

        r = "".join(rev)

        return r
```

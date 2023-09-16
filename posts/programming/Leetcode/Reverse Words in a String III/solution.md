<h3> Reverse Words in a String III </h3>

![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/862a1e29-ec84-42c8-b925-5ea5b95aa4e5)

Given a string `s`, reverse the order of characters in each word within a sentence while still preserving whitespace and initial word order.

To solve this I just converted the words in the string to a list and then iterate through the list and reverse the characters, then returned it's reformed value

Solve Script: [link](https://github.com/h4ckyou/h4ckyou.github.io/blob/main/posts/programming/Leetcode/Reverse%20Words%20in%20a%20String%20III/solve.py)
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/014a088b-9f47-4599-9ee8-e3b738f87fe0)


#### Leetcode Submission Script

```python
class Solution:
    def reverseWords(self, s: str) -> str:
        arr = s.split()
        r = []

        for i in range(len(arr)):
            r.append(arr[i][::-1])

        return " ".join(r)

```

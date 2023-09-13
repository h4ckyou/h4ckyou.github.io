<h3> Valid Palindrome </h3>

![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/14b415f8-86ee-4630-84e1-8807b46d7a45)

1. We will be given a string and we're asked to return True if the string is palindrome after passing a conditon else False.
2. The condition is that the uppercase letters should be converted to lowercase and all non-alphanumeric characters are removed. 
3. For it to be palindrome means that when it reads the same forward and backward.
4. To solve this I'll first need to take care of the conditions before checking if it's palindrome.
5. To check if it's palindrome I will implement linear search sort of approach to compare each character from the left to the right `array[left] != array[right]` 

Solve Script: [link](https://github.com/h4ckyou/h4ckyou.github.io/blob/main/posts/programming/Leetcode/Valid%20Palindrome/solve.py)
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/5bf61bb6-176a-4b63-aca7-93db35d16032)

Ehhhh it isn't optimized

After submitting the solution and looking at other people solution I saw an interesting approach:

Here's the approach:

The person made use of `isalnum()` which I didn't know existed (this would have made my condition check a bit faster!) also instead of using like linear search approach he made use of Not `~` operator

Operator `~` is the bitwise `NOT` operator `(~x == -x-1 => ~0 == -1 => ~1 == -2 and etc)`, which expects just one argument. It performs logical negation on a given number by flipping all of its bits:

Here's the script

```python
class Solution:
    def isPalindrome(self, s: str) -> bool:
        s = [c.lower() for c in s if c.isalnum()]
        return all (s[i] == s[~i] for i in range(len(s)//2))
```

Running it works
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/b038cb6d-6a36-4a28-af9f-22b4a96aa720)

Compared to mine in terms of space complexity, mine is better but in terms of time complexity that one is better

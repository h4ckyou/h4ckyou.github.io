<h3> Valid Palindrome II </h3>

![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/ea9909f1-20ab-4847-a1b7-b06fab4577c8)

We are given a string `s` and we are to return `True` if `s` is palindrome after deleting at most one character from it

Let's take a sample:

```
s = aba
```

Remember that when a word is said to be palindrome means that when we read it either forward or backward it reads the same

Now in this case the condition if to remove at most one character from it, so that means before we check is it's palindrome we need to remove any single character from the string

Let's say I remove the first character `a` the resulting string would be `ba` 

Is `ba` palindrome? Nope because it can't be read forward & backward

Let's remove the second string `b` the resulting string would be `aa` 

Is `aa` palindrome? Yup because it can be read forward and backward

From the previous `Palindrome` challenges I solved them using like linear search approach where I checked if the `array[left != array[right]`

Now I will implement it here too but now we need to make sure that we delete a character from the string

That can be achieved by incrementing the `left` pointer by `1` while the `right` pointer remains the same or decreasing the `right` pointer by 1 and the `left` pointer remains the same

Here's my solve script

Solve Script: [link](https://github.com/h4ckyou/h4ckyou.github.io/blob/main/posts/programming/Leetcode/Valid%20Palindrome%20II/solve.py)
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/9af43b05-f809-4edb-87ca-3b8b1183be39)

Complexity:
- Time complexity is `O(N)`
- Space complexity is `O(1)`

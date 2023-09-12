<h3> Roman To Integer </h3>

![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/7d424e03-d254-48c8-a901-d0189b2949bf)
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/90aed567-1490-4567-8f17-7b6a017e38ed)

The key intuition lies in the fact that in Roman Numerals, when a smaller value appears before a larger value, it represents subtraction, while when a smaller value appears after or equal to a larger value, it represents addition.

##### Explanation:
- The unordered map `m` is created and initialized with mappings between Roman numeral characters and their corresponding integer values. For example, `'I'` is mapped to `1`, `'V'` to `5`, `'X'` to `10`, and so on.
- The variable `ans` is initialized to `0`. This variable will accumulate the final integer value of the Roman numeral string.
- The for loop iterates over each character in the input string `s`.
  ##### Taking `IX` as the test case
  - When `i` is `0`, the current character `s[i]` is `'I'`. Since there is a next character `('X')`, and the value of `'I'` `(1)` is less than the value of `'X' (10)`, the condition `m[s[i]] < m[s[i+1]]` is true. In this case, we subtract the value of the current character from ans.

```
    ans -= m[s[i]];
    ans -= m['I'];
    ans -= 1;
    ans becomes -1.
```
  - When `i` is `1`, the current character `s[i]` is `'X'`. This is the last character in the string, so there is no next character to compare. Since there is no next character, we don't need to evaluate the condition. In this case, we add the value of the current character to ans.

```
    ans += m[s[i]];
    ans += m['X'];
    ans += 10;
    ans becomes 9.
```
  ##### Taking `XI` as the test case
  - When `i` is `0`, the current character `s[i]` is 'X'. Since there is a next character ('I'), and the value of 'X' (10) is greater than the value of 'I' (1), the condition `m[s[i]] < m[s[i+1]]` is false. In this case, we add the value of the current character to ans.

```
    ans += m[s[i]];
    ans += m['X'];
    ans += 10;
    ans becomes 10.
```
  - When `i` is 1, the current character `s[i]` is 'I'. This is the last character in the string, so there is no next character to compare. Since there is no next character, we don't need to evaluate the condition. In this case, we add the value of the current character to ans.

```
    ans += m[s[i]];
    ans += m['I'];
    ans += 1;
    ans becomes 11.
```

- After the for loop, the accumulated value in ans represents the integer conversion of the Roman numeral string, and it is returned as the result.

Solve Script: [link](https://github.com/h4ckyou/h4ckyou.github.io/blob/main/posts/programming/Leetcode/Roman%20To%20Integer/solve.py)
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/470327c4-2df0-4482-a266-e733377833f4)


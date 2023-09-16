<h3> Reverse Vowels of a String </h3>

![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/79bd7f2c-fa52-415d-bdfd-58e3d7980cfc)

Given a string `s`, reverse only all the vowels in the string and return it.

The vowels are `a`, `e`, `i`, `o`, and `u`, and they can appear in both lower and upper cases, more than once.

My approach:

We know that we'll be given a string `s` and our goal is to reverse only all the vowels in the string and return it

If you look at the example it's more of they swap the vowels where it's occurring in the left and right side of the string:

```
Input: s = "hello"
Output: "holle"
```

So I wrote a script to do the same thing and here's what it does:
- Store the vowel alphabet in a hashtable 
- Initialize two pointers `left` and `right` which would hold the `0th` and last index `len(s)-1`
- In a while loop I'll check the conditions:
  - To check for if the value of `s[left]` of the string is not a vowel I'll make a while loop that checks for that and I'll increment the `left` pointer by `1`
  - To check for if the value of `s[right]` of the string is not a vowel I'll make a while loop that checks for that and I'll decrement the `right` pointer by `1`
  - The point at which they exist two values where `s[left]` and `s[right]` is vowel I'll then swap them i.e set `s[left], s[right] =  s[right], s[left]`
  - Then I'll increment the `left` pointer by `1` and decrement the `right` pointer by `1` to keep the process going till I reach the condition where `left > right` then the loop finishes
 
Here's my solve script: [link](https://github.com/h4ckyou/h4ckyou.github.io/blob/main/posts/programming/Leetcode/Reverse%20Vowels%20of%20a%20String/solve.py)
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/98a6937d-a343-473e-83d7-64e42ae902bd)


#### Leetcode Submission Script

```python
class Solution:
    def reverseVowels(self, s: str) -> str:
        s = list(s)
        vowels = {"a", "e", "i", "o", "u", "A", "E", "I", "O", "U"}

        left, right = 0, len(s)-1

        while left < right:

            while left < right and s[left] not in vowels:
                left += 1

            while left < right and s[right] not in vowels:
                right -= 1
            
            if s[left] in vowels and s[right] in vowels:
                s[left], s[right] = s[right], s[left]


            left += 1
            right -= 1


        r = "".join(s)
        
        return r
```

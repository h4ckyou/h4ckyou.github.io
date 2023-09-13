<h3> Valid Palindrome </h3>

![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/14b415f8-86ee-4630-84e1-8807b46d7a45)

1. We will be given a string and we're asked to return True is the string is palindrome after passing a conditon else False.
2. The condition is that the uppercase letters should be converted to lowercase and all non-alphanumeric characters are removed. 
3. For it to be palindrome means that when it reads the same forward and backward.
4. To solve this I'll first need to take care of the conditions before checking if it's palindrome.
5. To check if it's palindrome I will implement binary search like sort of approach to compare each character from the left to the right `array[left] != array[right]` 

Solve Script: [link](https://github.com/h4ckyou/h4ckyou.github.io/blob/main/posts/programming/Leetcode/Valid%20Palindrome/solve.py)
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/5bf61bb6-176a-4b63-aca7-93db35d16032)

Ehhhh it isn't optimized

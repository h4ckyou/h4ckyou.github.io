<h3> Check if Strings Can be Made Equal With Operations I </h3>

![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/f77cf4a5-a4a4-4c8d-adc0-b17ffa6f5d53)

Here's is my thought process while I was trying to solve it:

1. We are given two strings of length 4 which are lowercase English letters
2. We are allowed to apply this operation on any of the two strings any number of times
	- We can choose two indices `i` and `j` such that `j - i = 2`, then if that works we will swap the two characters at those indices in the string
3. If we're able to make the two string equal we should return true else we'll return false

Solve Script: [link](https://github.com/h4ckyou/h4ckyou.github.io/blob/main/posts/programming/Leetcode/Check%20if%20Strings%20Can%20be%20Made%20Equal%20With%20Operations%20I/solve.py)

This is the idea behind my solve script:

First I figured that from the constraint the length of the string will be always 4

Then if I'm to find two indices such that `j - i = 2` therefore the value of `j` would be always greater than `i`

And from the length of the string there can be only two ways for us to meet that conditio

What that means is that at index `0` and `2` or `3` and `1` is that index value which would always meet that condition

Now for the swapping part what I did was to find all the values that can be swapped from the two possiblities

Then I'll the swapped value again

I just did that twice because I noticed upon swapping three times it would likely return it's initial value

So then I check if the second string is among the list of swapped values and if it is then I return True else False

The script works but it isn't quite efficient
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/fb4348d5-223d-409e-ab11-9d61a1a282e8)

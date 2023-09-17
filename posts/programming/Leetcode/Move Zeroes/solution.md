<h3> Move Zeroes </h3>

![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/c5220b25-cd32-4e48-9a63-bfe6227d2afe)

We have an integer array that may or may not have some zeroes. 

Our goal is to move all the zeroes to the right of the array without disturbing the original order of all the remaining elements. We desire a space complexity of `O(1)` since we're to solve this `in-place` meaning it won't use additional memory space

Thinking about the problem a little more, we do not have to do anything with the zeroes as long as we maintain the relative order of the other elements.

This signals firstly that we do not need any extra space to store the zero's

A very simple approach will be:
- Start from the first element in the array, and keep a marker.
- For an element that is non-zero, move the marker ahead as we want to keep the number.
- If the element is zero, just move ahead in the array and leave the marker in the original place.
- Iterate through each element and apply the same logic at every element
- If the array had only 3 non-zero elements, the marker will be at the third position in the array.
- All the rest elements can be substituted with a 0

This method will work `in-place` without taking any extra space.

Solve Script: [link](https://github.com/h4ckyou/h4ckyou.github.io/blob/main/posts/programming/Leetcode/Move%20Zeroes/solve.py)
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/f3248bd1-eb8b-4634-874e-de3f45f2ae7d)

<h3> Minimum Common Value </h3>

![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/ac976d83-4192-4173-99c2-53454fadc47c)

My thought process!

1. We are given two arrays and we're asked to find the minimum common value in the two arrays
2. Iterate through the list of lower size and binary search each element in the other array
3. If found i'll return the value since it's the first mininmum common value

Solution Script: [link](https://github.com/h4ckyou/h4ckyou.github.io/blob/main/posts/programming/Leetcode/Minimum%20Common%20Value/solve.py)

Well my script in terms of speed takes quite some time since I'm literally going over each elements in the first array.
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/9d703cfc-4158-4180-af4b-2ac8ada13a52)

If I'm to take the worst case scenerio I'll have to loop through at least `100,000` elements in the array

Or performing binary search for a number as large as `1000000000` but that isn't a big deal cause the time complexity of binary search is `0(log N)` while the other is more of like linear search whose complexity is `O(N)`

Another way I found is to use Two Pointers approach:

Here's what that does:
- Iterate through array1 and array2:
  - If `array1[i]` < `array2[j]` then it will increment `i` by 1
  - Else it will increment `j` by 1
  - Else return `array1[i]`

The idea behind that is that it will get a number from the first array whereby no elements in the second array will be less than or greater than the chosen number in array1

That works because both arrays are sorted

Here's the script: [link](https://github.com/h4ckyou/h4ckyou.github.io/blob/main/posts/programming/Leetcode/Minimum%20Common%20Value/solve2.py)

Running it shows it is more effective than my previous solve script
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/2aa89360-cbb6-47a1-919b-0e11f385cfbe)

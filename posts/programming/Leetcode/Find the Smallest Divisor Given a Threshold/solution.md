<h3> Find the Smallest Divisor Given a Threshold </h3>

![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/5696e15e-ce37-4b75-9c0c-bb87bdb290c6)

We are given an array `nums` with an integer `threshold`. Our goal is to find a positive integer `divisor` which would divide all the elements in the array by it. If the sum of all the result is less than or equal to the `threshold` we should return the smallest divisor value

One thing we should note there is that the value of `divisor` does not nessary means it has to belong to the arrary `nums` as it can be greater than the maximum value in the array

Here's the first approach I took in solving this:
- I noticed that the maximum value in the array when used as the `divisor` with the conditon in tact tends to be either less than or equal to the `threshold` value. What that means is that if the divisor used is the maximum value, when we then calculate the sum i.e *`array[i] / divisor`* the result tends to be less than or equal to the threshold value. So that means that the lower the value the higher the sum tends to be greater than the threshold value
- With that I was able to implement binary search to keep finding a number from the right hand side of the array (I sorted the array) so that I meet the condition
- But the issue I faced was that I was implementing the search based on the array but what if the threshold value is greater than each elements in the array that would make my script fail
- So I then optimized it to set the initial search space dynamically that means instead of me to base the right pointer on the length of the array `len(array)-1` I made set it to a value that is a multiple of the maximum element in the array and the threshold `max(array) * threshold`. Using that it allows the search to continue until it finds the smallest divisor that satisfies the condition, even if the threshold is greater than any element in the array.

Solve Script: [link](https://github.com/h4ckyou/h4ckyou.github.io/blob/main/posts/programming/Leetcode/Find%20the%20Smallest%20Divisor%20Given%20a%20Threshold/solve.py)
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/dbc6e825-45f0-41c9-a1cc-e954bd762eb0)


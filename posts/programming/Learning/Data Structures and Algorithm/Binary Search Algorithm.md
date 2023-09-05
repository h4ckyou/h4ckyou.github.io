<h3> Binary Search Algorithm </h3>

Binary Search is defined as a searching algorithm used in a sorted array by repeatedly dividing the search interval in half. The idea of binary search is to use the information that the array is sorted and reduce the time complexity to O(log N). 
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/fd62102c-2206-4b4c-ad3b-317bf6f99425)

Conditions for when to apply Binary Search in a Data Structure:

To apply Binary Search algorithm:
- The data structure must be sorted.
- Access to any element of the data structure takes constant time.

Binary Search Algorithm:

In this algorithm, 
- Divide the search space into two halves by finding the middle index "mid". 
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/22ba339c-76c5-42b2-a88e-cd1f6e65009d)
- Compare the middle element of the search space with the key. 
- If the key is found at middle element, the process is terminated.
- If the key is not found at middle element, choose which half will be used as the next search space.
  - If the key is smaller than the middle element, then the left side is used for next search.
  - If the key is larger than the middle element, then the right side is used for next search.
- This process is continued until the key is found or the total search space is exhausted.

  

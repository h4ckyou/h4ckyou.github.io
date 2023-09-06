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

How to Implement Binary Search?

The Binary Search Algorithm can be implemented in the following two ways
- Iterative Binary Search Algorithm
- Recursive Binary Search Algorithm

Complexity Analysis of Binary Search:

Time Complexity: 
- Best Case: O(1)
- Average Case: O(log N)
- Worst Case: O(log N)

Auxiliary Space: O(1), If the recursive call stack is considered then the auxiliary space will be O(logN).

Advantages of Binary Search:
- Binary search is faster than linear search, especially for large arrays.
- More efficient than other searching algorithms with a similar time complexity, such as interpolation search or exponential search.
- Binary search is well-suited for searching large datasets that are stored in external memory, such as on a hard drive or in the cloud.

Drawbacks of Binary Search:
- The array should be sorted.
- Binary search requires that the data structure being searched be stored in contiguous memory locations. 
- Binary search requires that the elements of the array be comparable, meaning that they must be able to be ordered.

Applications of Binary Search:
- Binary search can be used as a building block for more complex algorithms used in machine learning, such as algorithms for training neural networks or finding the optimal hyperparameters for a model.
- It can be used for searching in computer graphics such as algorithms for ray tracing or texture mapping.
- It can be used for searching a database.

SOURCE: [GeeksForGeeks](https://www.geeksforgeeks.org/binary-search/)

#### Example
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/9bbd3097-bbce-42fb-930f-55072f8ef15f)






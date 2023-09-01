<h3> Linear Search Algorithm </h3>

Explanation: 

Linear Search is defined as a sequential search algorithm that starts at one end and goes through each element of a list until the desired element is found, otherwise the search continues till the end of the data set.

![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/75a6ca80-00b2-4905-918b-f0a07b06cae7)

How Does Linear Search Algorithm Work?

In Linear Search Algorithm:
- Every element is considered as a potential match for the key and checked for the same.
- If any element is found equal to the key, the search is successful and the index of that element is returned.
- If no element is found equal to the key, the search yields “No match found”.

Complexity Analysis of Linear Search:

Time Complexity:

    Best Case: In the best case, the key might be present at the first index. So the best case complexity is O(1)
    Worst Case: In the worst case, the key might be present at the last index i.e., opposite to the end from which the search has started in the list. So the worst-case complexity is O(N) where N is the size of the list.
    Average Case: O(N)

Auxiliary Space: O(1) as except for the variable to iterate through the list, no other variable is used. 

Advantages of Linear Search:
- Linear search can be used irrespective of whether the array is sorted or not. It can be used on arrays of any data type.
- Does not require any additional memory.
- It is a well-suited algorithm for small datasets.

Drawbacks of Linear Search:
- Linear search has a time complexity of O(N), which in turn makes it slow for large datasets.
-  Not suitable for large arrays.

When to use Linear Search?
- When we are dealing with a small dataset.
- When you are searching for a dataset stored in contiguous memory.

#### Example:

Given an array Arr of N elements and a integer K. Your task is to return the position of first occurence of K in the given array.

Note: Position of first element is considered as 1.

Your Task:
Complete the function `search()` which takes an array arr, two integers n and k, as input parameters and returns an integer denoting the answer. Return -1 if the number is not found in array. You don't to print answer or take inputs.

Expected Time Complexity: O(N)
Expected Auxiliary Space: O(1)

Constraints:
```
1 <= N <= 10^6
1 <= K <= 10^6
1 <= Arr[i] <= 10^6
```

Parameters given:

```
K = 16
Arr[] = {9, 7, 2, 16, 4, 5, 1, 3, 10, 25, 31, 45, 60, 200}
```

To solve this I'll implement Linear Search Algorithm since the dataset array is not large:

Here's my solve script:

```python
# Linear Search Algorithm

def search(arr, N, k):
    idx = 1
    position = 0

    for i in range(1, N+1):
        if arr[i - idx] == k:
            position = i
            break
        else:
            position = -1
    
    return position

arr = [9, 7, 2, 16, 4, 5, 1, 3, 10, 25, 31, 45, 60, 200]
N = len(arr)
k = 16

res = search(arr, N, k)
print(res)
```

It works!

![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/59d0e8c2-83a1-4275-9a9d-e7980b89de5f)










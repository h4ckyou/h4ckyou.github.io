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

#### Example 1:
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/9bbd3097-bbce-42fb-930f-55072f8ef15f)

Given an array of integers nums which is sorted in ascending order, and an integer target, write a function to search target in nums. If target exists, then return its index. Otherwise, return -1.

Let us look at the first example case they gave us:

```
Input: nums = [-1,0,3,5,9,12], target = 9
Output: 4
Explanation: 9 exists in nums and its index is 4
```

So we are to find the index position of a target value in an array

The best algorithm to use here of cause is Binary Search because the list is sorted 

First thing we need is this:

```
L = 0
R = len(nums) - 1
mid = L + (R - L) // 2
target = 9
```

Now we will start from the center of the array:

```
[-1,0,3,5,9,12]
```

The center index of the array is 3

![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/fcaf2ea3-6b98-4b2c-ac31-1d454744b436)

```
>>> nums = [-1,0,3,5,9,12]
>>> L = 0
>>> R = len(nums) - 1
>>> mid = L + (R - L) // 2
>>> target = 9
>>> 
>>> nums[mid]
3
>>>
```

Now we check the condition:
- Is the array index of the middle number equal to the target value? If it is return the middle number!
- Is the array index of the middle number less than the target value? If it is shift the search space to the right by setting `L` to `mid + 1` and repeating the process!
- Is the array index of the middle number greater than the target value? If it is shift the search space to the left by setting `R` to `mid - 1` and repeating the process!

That's the logic of `Iterative Binary Search Algorithm` since we will be doing this in a loop and not recursively

Doing that manually wouldn't take time since this array is small in terms of the length

But it's best to put your coding skill in practice

So I wrote a script to solve that!

Here's the script:

```python
# Iterative Binary Search Algorithm

def binarySearch(arr, x):
    l = 0
    r = len(arr)-1

    while l <= r:
        
        mid = l + (r - l) // 2

        if arr[mid] == x:
            return mid

        elif arr[mid] < x:
            l = mid + 1

        else:
            r = mid - 1
        
    return -1


arr = [-1,0,3,5,9,12]
x = 9

result = binarySearch(arr, x)
print(result)
```

Using it I got the value of the target which is 4
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/5f39e2cf-9663-4fc5-a1da-056411bb65c2)


We can run the script and use the other case sample
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/66192e51-2fd3-4812-9caf-ae66dba0112d)
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/49dd9e6e-b346-446f-bbae-b101c31cefca)

It returned `-1` because the target value we are searching for isn't among the array

Here's a sample script using Recursive Binary Search

```python
# Recursive Binary Search Algorithm

def binarySearch(arr, x, l, r):
    mid = l + (r-l)//2

    while r >= 0:

        if arr[mid] == x:
            return mid
        
        elif arr[mid] < x:
            return binarySearch(arr, x, l+1, r)
        
        else:
            return binarySearch(arr, x, l, mid-1)


arr = [-1,0,3,5,9,12]
x = 9
l = 0
r = len(arr)-1

result = binarySearch(arr, x, l, r)
print(result)
```

Now that we have a working solution we can now use the submission template and write the code there
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/6a80459c-b491-4db8-93e9-1e72f97ec148)

Wait what `Time Limit Exceeded`!!

Is python this slow for their time complexity?

But it takes very less seconds when I run it on my laptop
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/791d13c8-b37a-4f28-a3f1-f429788ea3b8)

Well since it's their custom Class they maybe will add some time complexity which my program didn't succeed in passing it

Now what?

Well I moved to C++ since it's more faster 

Here's the code

```cpp
class Solution {
public:
    int search(vector<int>& nums, int target) {
        int n = nums.size();
        int r = n - 1;
        int l = 0;
        
        while (l <= r) {
            int m = l + (r - l) / 2; 
            
            if (nums[m] == target)
                return m;
            
            if (nums[m] < target)
                l = m + 1;
            
            else
                r = m - 1;
        }
        
        return -1; 
    }
};
```

Running it I passed the custom testcase with a program runtime of 0ms 
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/c814ee4e-26a2-471c-85e6-797172edab41)

Now I can submit the code and boom it worked!
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/33e41211-36d7-4383-a9f8-27e11fbcea04)

I was wondering why python didn't work so I checked the script and found a bug :(
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/90ad4f96-90f6-4ab1-9758-8575e6eaf9bc)

The middle variable is supposed to be inside the while loop
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/c3c1abd6-fbc5-4421-9cf1-1f355cb608b1)

So after making that edit it worked
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/534bb318-b4f8-48cb-b75e-ac4d2ac26bca)

But still C++ is pretty much faster 🙂

#### Example 2
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/5ccb974f-9391-4ff1-b640-228d72a8b6c5)

Given a non-negative integer x, return the square root of x rounded down to the nearest integer. The returned integer should be non-negative as well.

You must not use any built-in exponent function or operator.

For example, do not use pow(x, 0.5) in c++ or x ** 0.5 in python.

Ok so the question is pretty understandable!

We are going to be given a non-negative integer `x` and we are to provide the square root without using any builtins function like pow()

This seemed intimidating to me at first when I tried it but after few minutes of thinking I got a breakthrough


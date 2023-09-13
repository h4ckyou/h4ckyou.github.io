<h3> 4Sum II </h3>

![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/d9f8c833-c255-487f-b01f-2b3b4ef28600)

We will be given four different arrays `nums1, nums2, nums3, nums4` all of the same length

Our goal is to return the number of tuples `(i, j, k, l)` such that:

```
- 0 <= i, j, k, l < n
- nums1[i] + nums2[j] + nums3[k] + nums4[l] == 0
```

I used two approach to solve this

##### Approach 1

The first approach implements the use of brute force where I'll basically go through nested loops in order to find a value such that when I sum the each array with the corresponding iterate it gives `0`

The idea is this:

Let's take a sample

```
nums1, nums2, nums3, nums4 = [1, 2], [-2, -1], [-1, 2], [0, 2]
```

I'll go through the first element in the first array and check the condition for each other elements in the other arrays i.e

```
nums1[0] + nums2[0] + nums3[0] + nums4[0] == 0
nums1[0] + nums2[0] + nums3[0] + nums4[1] == 0
nums1[0] + nums2[0] + nums3[1] + nums4[0] == 0
nums1[0] + nums2[0] + nums3[1] + nums4[1] == 0
nums1[0] + nums2[1] + nums3[0] + nums4[0] == 0
nums1[0] + nums2[1] + nums3[0] + nums4[1] == 0
nums1[0] + nums2[1] + nums3[1] + nums4[0] == 0
nums1[0] + nums2[1] + nums3[1] + nums4[1] == 0
```

Next if I find a value I'll increment the `count` variable by `1` and now use the second element in the first array and iterate through other elements in the other array i.e

```
nums1[1] + nums2[0] + nums3[0] + nums4[0] == 0
nums1[1] + nums2[0] + nums3[0] + nums4[1] == 0
nums1[1] + nums2[0] + nums3[1] + nums4[0] == 0
nums1[1] + nums2[0] + nums3[1] + nums4[1] == 0
nums1[1] + nums2[1] + nums3[0] + nums4[0] == 0
nums1[1] + nums2[1] + nums3[0] + nums4[1] == 0
nums1[1] + nums2[1] + nums3[1] + nums4[0] == 0
nums1[1] + nums2[1] + nums3[1] + nums4[1] == 0
```

After the loop finishes I'll return the value stored in my `count` variable

Here's my [script](https://github.com/h4ckyou/h4ckyou.github.io/blob/main/posts/programming/Leetcode/4Sum%20II/brute.py)

```python
def fourSumCount(nums1, nums2, nums3, nums4):
    n = len(nums1)
    count = 0 

    for i in range(n):
        for j in range(n):
            for k in range(n):
                for l in range(n):
                    sum = nums1[i] + nums2[j] + nums3[k] + nums4[l]

                    if sum == 0:
                        count += 1

    return count

nums1, nums2, nums3, nums4 = [1, 2], [-2, -1], [-1, 2], [0, 2]
r = fourSumCount(nums1, nums2, nums3, nums4)
print(r)
```

It works but now the issue is the time complexity

Remember the constaint is this:

```
- n == nums1.length
- n == nums2.length
- n == nums3.length
- n == nums4.length
- 1 <= n <= 200
- -228 <= nums1[i], nums2[i], nums3[i], nums4[i] <= 228
```

Basically the length of the array can be up to `200` and each elements in the array is in range `-228 to 228`

If we are to take the worst case scenerio i.e the array has length of `200` and each element is `228`

Because the time complexity is `O(n^4)` because we have four nested loops, each of which iterates `n` times. This means that the time it takes to run the code will increase significantly as the size of the input array `(nums1, nums2, nums3, nums4)` increases

It can be confirmed from this test case when I submitted it
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/29f1150d-f38a-4451-b82b-5b689357e9c6)

So at least now I understand the logic of this problem but need to create a more optimized solution

This lead to the second approach

##### Approach 2

The simple bruteforce solution would take `n^4` time complexity here.

We can do better by dividing given lists into two groups and precalculating all possible sums for the first group.

Results go to a hash table where keys are sums and values are frequencies. It will take `n^2` time and space. After that, we iterate over elements of the second group, and for every pair check whether their sum can add up to zero with a sum from the first group using a hash table.

In the script you would see this:

```
check = 0 - (nums3[k] + nums4[l])
```

Here's the explanation:

The sum of four numbers must add up to zero. Taking one index from every number, it would look like

```
nums1[i] + nums2[j] + nums3[k] + nums4[l] = 0 

Let's call this equation A.
```

We initially stored the sum of all possible sums of the first two arrays in a hashmap by doing:

```python
sum = nums1[i] + nums2[j]

if sum in hashtable:
    hashtable[sum] += 1
else:
    hashtable[sum] = 1
```

For example, let the first two arrays be `[1, 2]` and `[-2, -1]`. All possible sums are:

```
1 + (-2) = -1
1 + (-1) =  0
2 + (-2) = 0
2 + (-1) = 1
```

So the hashmap will look like this for this case:

```python
{
   0: 2
  -1: 1
   1: 1
}
```

Now, we can re-write equation `A` as:

```
nums1[i] + nums2[j] = 0 - (nums3[k] + nums4[l])
```

What I'm I doing? Well I'm moving the numbers from `nums3 & nums4` to the right side of the equation, thus changing their sign.

This translates that, if we find all cases where subtracting `(nums3[k] + nums4[l])` from `0` is equal to `(nums1[i] + nums2[j])`, we get the cases where the sum of the four numbers equals zero.

With that said the solve script is below :P

Complexity:
- Time complexity: `O(N^2)`
- Space complexity: `O(N^2)`

Here's the solve script: [link](https://github.com/h4ckyou/h4ckyou.github.io/blob/main/posts/programming/Leetcode/4Sum%20II/solve.py)
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/aa43b776-e901-4232-b78b-aef2a7e8f647)




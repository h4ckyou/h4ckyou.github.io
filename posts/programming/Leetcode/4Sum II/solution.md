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

Here's my script

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

If we are to take the worst case scenerio i.e the array has length of 228 and each element is 228

Because the time complexity is `O(n^4)` because we have four nested loops, each of which iterates `n` times. This means that the time it takes to run the code will increase significantly as the size of the input array `(nums1, nums2, nums3, nums4)` increases

It can be confirmed from this test case when I submitted it
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/29f1150d-f38a-4451-b82b-5b689357e9c6)

So at least now I understand the logic of this problem but need to create a more optimized solution

This lead to the second approach

##### Approach 2




<h3> 4Sum</h3>

![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/3d800ad1-2108-42ff-95d4-ee20ca97aa3c)

We are going to be given an array `nums` containing integers, our goal is to return an array of all the unique quadruplets `[nums[a], nums[b], nums[c], nums[d]]` such that:

```
- 0 <= a, b, c, d < n
- a, b, c, and d are distinct.
- nums[a] + nums[b] + nums[c] + nums[d] == target
```

In order to solve this I implemented Binary Search and what it will do is to find the `triplets` and `two pairs` that when summed will equal the `target` value

I won't bother about repeating values because I'll be using a hashset to store the result and hashset doesn't allow duplicates

One key thing we should note in my script is that the range I'm looping in

The first loop iterates through `len(array) - 3`

That's because we can only get the quadruplet when there are at least 4 elements in the array meaning the length must be at least 3

So let's say I have this array:

```
arr = [1, 2, 3, 4]
```

And we're asked to find the quadruplet for target `10` the answer is `[1, 2, 3, 4]` but if the length of the array is below 3 i.e `[1, 2, 3]`, there's no way we can get the quadruplets

The second loop iterates through `j+1, len(arr) - 2` now because I want to exclude searching for the first element on each iterate in order to not get a case where `i == j` (i.e this might cause the `sum` result to equal `target`) because the values must be unique so we must avoid using the same index value

Also since this portion finds the triplet the length of the array where it's searching must be at least 2

Let's take a case sample: If I have this array:

```
arr = [1, 2, 3]
```

And we're asked to find target value of `6` the answer is `[1, 2, 3]` but if the length of this array is below 2 i.e `[1, 2]` then we can't find it's triplet

While the last case is finding pairs which meet the condition:

```
array[j] + array[i] + array[left] + array[right] == target
```

With that we're done and we can just return the values

Here's my solve script: [link]()
 
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/3e825a8a-9c90-4364-bb87-04d1954a0e9c)

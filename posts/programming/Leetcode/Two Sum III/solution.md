<h3> 3Sum </h3>

![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/df9835f4-c50e-481e-beb5-3a22ec1d8a18)
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/5e93b771-c187-4fc0-81b2-01394a42b273)

We will be given an integer array `nums` our goal is to return all the triplets `[nums[i], nums[j], nums[k]]` such that `i != j`, `i != k`, and `j != k`, and `nums[i] + nums[j] + nums[k] == 0`

So our solution must not contain duplicate and also the situation where the indices `i,j` or `i,k` and `j,k` are the same isn't allowed

Here's my solve approach:
- First after sorting the array we need to find a way to get two pairs whereby their sum with target gives `0`

What does that mean?

Let's take this example:

```
nums = [-4, -1, -1, 0, 1, 2]
```

I'll iterate through `nums` and let's take the first index as target value:

If we're to cut out the first index which we choose the remaining array would be:

```
nums = [-1, -1, 0, 1, 2]
```

Using binary search I can get two pairs from the array that when summed up with target which in this case is `-4` will give `0`

I'll have to take care of duplicate both in the left and right search space

With that the result returned if we try find a pair would be:

```
result = []
```

Now I'll move to the next value in the array:

```
target = -1
nums = [-1, 0, 1, 2]
```

Apply the same implementation to get the right pairs and eventually we would reach this:

```
target = 0
nums = [1, 2]
```

Looking at this we should probably stop our loop because we can't find triplets if the values there are just two elements therefore our loop would be within range `len(array)-2`

With that said my solve script is in the below link 🙂

Solve Script: [link](https://github.com/h4ckyou/h4ckyou.github.io/blob/main/posts/programming/Leetcode/Two%20Sum%20III/solve.py)
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/5f5ffd97-4127-4c6d-9777-e5d6b4cdd2aa)

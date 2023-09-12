<h3> Contains Duplicate II </h3>

![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/4422d344-3dfa-458c-8e08-02335c965cf8)

From the first challenge of this series `Contains Duplicate` I learnt a more efficient way of getting duplicates in an array so I just implemented it here and of cause made sure it meet the conditions

Here is my thought process:

```
1. We are given an array named `nums` and an integer named `k`
2. We are to return true or false based on the following conditions:
	- If there are two distinct indices `i & j` where by nums[i] == nums[j] and abs(i - j) <= k
	- We should return true else we will return false
3. I'll create a hash table that would hold up the elements as keys and their indices as values
4. Then use the condition required by the program
```

Solve Script: [link](https://github.com/h4ckyou/h4ckyou.github.io/blob/main/posts/programming/Leetcode/Contains%20Duplicate%20II/solve.py)

Running it works meeting a very low time complexity compared to other python scripters
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/260ee4ce-db35-409c-9860-bf6e05b85fa3)

So here's the explanation to my solve script

- I create a hash table which would hold up the elements of the array with it's corresponding index
- While I'm on that loop of creation I'll check if there has been any occurrence of the current element
  - If that is True then I'll calculate the absolute value of the current iterate with the index value of the element already in the hash table
  - If the value is less than or equal to `k` then I'll return True
- But if that's not the case then I'll keep on adding elements and it's index to the hashtable till I exhaust the whole elements in the array


  

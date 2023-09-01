<h3>Missing Number </h3>

![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/1d51fec6-84e5-4e96-81f3-2817c2c28f9e)

Description:

```
You are given all numbers between 1,2,…,n except one. Your task is to find the missing number.
```

Constraint:

```
2 ≤ n ≤ 2⋅10^5
```

So the first input will be an integer `n`

The second input will consist of number within range `n - 1` where each number is distinct and between 1 and n (inclusive)

The goal for our algorithm is to find the missing number

This are the conditions:

```
Time Limit: 1.00s
Memory Limit: 512MB
```

My first approach is this:
- Make the second input as an array and sort it in terms of ascending order
- Define a function to loop through the highest value (i.e the first integer) then checks if the iterate is not among the array
- if that's the case then it's the missing number

Here's the script

```python
def search(array, last):
    missing = []
    for i in range(last+1):
        if str(i) not in array:
            missing.append(i)

    return missing[1]

n1 = int(input())
n2 = sorted(input().split())

r = search(n2, n1)
print(r)
```

It works but the time limit was exceeded

![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/fb80bac9-5f24-4bd2-9d38-ebfd59c7efe8)

Well that's expected cause looping through large number has it's cons which includes the time complexity 🙂

So I thought of another way to make this more efficient and here's my final solution

<h3> Weird Algorithm </h3>

![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/f796d484-7853-4afe-947b-6bb60b36ab4f)

We are given the description as:

```
Consider an algorithm that takes as input a positive integer n.
If n is even, the algorithm divides it by two, and if n is odd, the algorithm multiplies it by three and adds one.
The algorithm repeats this, until n is one.

For example, the sequence for n=3 is as follows:
3 → 10 → 5 → 16 → 8 → 4 → 2 → 1
```

The constraint is:

```
1 ≤ n ≤ 10^6
```

So we're to create an algorithm that does this:
- When given a positive integer `n` provided as the input, it will check this:
  - If the number provided is an even number it will divide it by 2
  - If it's an odd number it will multiply it by 3 and add one to it
  - The program will do this till `n` is 1

Here's my solve script:

```python
def algo(n):
    r = [n]
    try:
        while r[-1] != 1:
            if n % 2 == 0:
                n = n // 2
            else:
                n = (n * 3) + 1
            r.append(n)
    except Exception:
        pass

    return r

n = int(input())
sequence = algo(n)
print(" ".join(map(str, sequence)))
```

Basically what it does is this:
- Defines a function called `algo` which requires a number passed as the argument
  - It sets the array `r` with the number passed into this function
  - It will start a while loop that checks if the last number of the list is not equal to `1`
  - If it isn't then it checks if the number is even or odd then performs the expected operation
  - The result is then appended to the array
  - And while the result isn't returning 1 the loop will continue
- The final result is going to be returned as a list
- Then using `map` I set it to the expected output required for this algorithm question

Here's the result 
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/cab21dc7-8a76-48cd-a0b0-6a9b8aefca37)

Btw the failed attempt is when I was trying to upload an empty script :D

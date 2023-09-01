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

The contraint is:

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

<h3> Constrained </h4>

![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/208ff74c-1513-412b-ad29-99795b850e4c)

A fun easy one.... let's get to it.

We are given a python 3.6 byte compiled code
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/f3933fbf-d0e4-423d-92e1-155dfb52e46b)

To decompile it I used [pycdc](https://github.com/zrax/pycdc)
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/bf67e553-fc24-47a2-986b-d4c21955b299)
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/ca36b98e-1956-44b1-beb4-4e3ee5632f85)

This is the main logic of the code:

```python
def check(flag):
    if len(flag) != 52:
        return False
    None.seed(1337)
    for i in range(56):
        a = random.randint(0, 51)
        b = random.randint(0, 51)
        c = random.randint(0, 51)
        d = random.randint(0, 51)
        t = ((flag[a] << 8) + flag[b]) * ((flag[c] << 8) + flag[d]) & 65535
        if t != magic[i]:
            return False
    
    return True

if __name__ == '__main__':
    flag = input('Flag: ').encode('ascii')
    if check(flag):
        print('Correct!')
    else:
        print('Wrong!')
```

So it tends to be a flag checker where we need to get the correct flag 

Let me go through what it does exactly:
- First it receives our input which is supposed to be "flag"
- It then calls the check() function passing our input as the parameter

This is what the check() function does:
- It checks if the length of our input is 52 and if it isn't the program returns False thus giving us the error message "Wrong!"
- Else it would seed the random function with 1337. Note that the module was imported `import random`
- For the encryption part:
  - It generates 4 random integers within 0-51 where each one are stored in variable `a, b, c, d` respectively
  - Then it generates the encrypted flag character `t` with `t = ((flag[a] << 8) + flag[b]) * ((flag[c] << 8) + flag[d]) & 65535`
  - Basically that just does some `Bit Left Shifting, Addition, Multiplication` and a `AND` operation
  - Then it compares the generated encrypted value with the magic array on the current index `magic[i]`
  - This process is done 56 times
 

So to solve this challenge I made use of an [SMT](https://en.wikipedia.org/wiki/Satisfiability_modulo_theories) solver called [z3](https://github.com/Z3Prover/z3)

One thing to note is that when the random module is seeded it becomes "broken" when the seed is known because it isn't more "predictable (random)". That means we can also generate the next random value since the seed is known making it easier, though with using z3 it doesn't matter as to whether the seed is known it would find the right value provided that the constraint is satisfiable






















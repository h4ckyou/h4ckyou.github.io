<h3> Constrained </h3>

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

One thing to note is that when the random module is seeded it becomes "broken" when the seed is known because it isn't more "predictable (random)". That means we can also generate the next random value since the seed is known making it easier, though with using z3 it doesn't matter as to whether the seed is known it would find the right value provided that the constraint is satisfiable.

Here's my solve script:

```python
from z3 import *
from random import randint

magic = [6596, 29872, 62287, 15227, 36671, 60341, 63931, 1709, 41434, 63916, 60583, 25325, 38705, 55592, 60787, 38714, 17528, 44216, 27185, 8035, 15695, 26256, 40808, 56784, 29555, 46895, 34850, 64576, 18532, 144, 31896, 4615, 17391, 26277, 32664, 8643, 13327, 16877, 43771, 54171, 59881, 62544, 54976, 10049, 30360, 9514, 26232, 21331, 17184, 2651, 63297, 1680, 54032, 43896, 6491, 56666, 48037]
flag = [BitVec(f'f_{i}', 8) for i in range(52)]
s = Solver()

for i in flag:
    s.add(i > 0x20)
    s.add(i < 0x7f)


for i in range(56):
    a = randint(0, 51)
    b = randint(0, 51)
    c = randint(0, 51)
    d = randint(0, 51)
    t = ((flag[a] << 8) + flag[b]) * ((flag[c] << 8) + flag[d]) & 65535

    s.add(t == magic[i])


if s.check() == sat:
    m = s.model()
    w = ''

    for i in range(len(flag)):
        w += chr(m[flag[i]].as_long())

    print(w)
```

In my script I made sure that the result z3 should find would be within the ASCII range
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/a6ab4d30-b136-4d61-b585-e5fd727020b0)
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/83b4a3da-eab7-4567-b990-8df073292c03)

Running it works?
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/33269640-f193-414d-83b6-177c32cf7c4f)

We can confirm if it's right by passing it as the input to the decompiled program
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/2cfc0996-01af-4847-992e-8fbd958b4e01)

But still when I submitted it, i got error that it's the wrong flag....but why 🤔

Reading the flag I saw this:

```
FlagY{w0w_I_hop3_9ou_used_z3_or_smth_01830193972983}
```

The right value should be:

```
FlagY{w0w_I_hop3_you_used_z3_or_smth_01830193972983}
```

And we can confirm it
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/de2d3aa8-e089-46c9-909c-e2dc1cd497ce)

Just to guess that wrong character so it wasn't much of a pain

And that's all..

Thanks for reading 😏



















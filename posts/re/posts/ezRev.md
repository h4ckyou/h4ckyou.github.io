#### Challenge:
    - Name: EzRev
    - Description: In and out of the matrix 🙂

The file attached to this challenge is a binary called `matrix`
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/bed56af0-99e3-4324-92b8-f63a2d040f12)

So we're working with a x64 executable and after running the binary it showed this
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/7f2fbaf1-f27a-4c4e-8bea-6a64caf1e45d)

It seems that it only requires an integer which will be provided 4 times and from the result of the output we need the right input to escape the matrix

Since there's nothing much that can be done here I loaded the binary up in Ghidra

Here's the main function
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/0efcd88e-9e5d-4ee9-abbf-7c31d45c4c28)

Since the variable names from the pseudocode isn't looking good I renamed it
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/722f5948-5898-43f7-b3b9-86e4fd350608)

Ok it's looking good but here's the part which does not look too nice to the eyes:

```c
*(int *)(matrix + ((long)k + (long)j * 4) * 4);
```

Inorder words that piece of code is equivalent to `matrix[j][k]` so this means the data type for the global variable `matrix` isn't right

So I checked it to know the length of the array

![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/39ca954b-9356-46da-84c9-889927f0b008)

The size is 64 and since the elements there are `DWORD --> int()` whose size is 4 bytes that means the number of elements there are 16

And from the 2 nested inner loop which defines `j and k` it iterates till it reaches 4 twice meaning the matrix is a 4x4 matrix i.e it has 4 rows and 4 columns

At this point I changed the data type of the global variable matrix to `int[4][4]` 

![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/02b4abc7-4aa6-4c8c-bdf6-36c5d4423b6a)

Now the pseudocode looks ok
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/87a7ef47-45b2-4f3d-bba5-2379d0030953)

```c

undefined8 main(void)

{
  undefined8 ret;
  int value [7];
  int sum;
  int c;
  int k;
  int j;
  int i;
  
  sum = 0;
  for (c = 0; c < 4; c = c + 1) {
    __isoc99_scanf("%d", &value[c]);
  }
  for (i = 0; i < 4; i = i + 1) {
    for (j = 0; j < 4; j = j + 1) {
      for (k = 0; k < 4; k = k + 1) {
        sum = sum + value[i] * matrix[j][k];
      }
    }
  }
  if (sum == check) {
    check_pass();
    ret = 0;
  }
  else {
    check_failed();
    ret = 0xffffffff;
  }
  return ret;
}
```

Now I'll explain what this does exactly

- First it would receive our input as an integer in a loop 4 times and the values are stored at the corresponding index position of the value array
- It defines a variable `sum` which initially holds the value `0` then in a 3 nested loop it does this:
      - Transverse over all the elements in the matrix, during the transversal it multiplies the elements by `value[i]` where the result is stored in the `sum` variable
      - The sum variable adds itself with the value returned by the operation on the next iterations 

Then after the loop is done the sum is compared with the value stored in the global variable `check` which is `0x00E00C4`
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/39d948d8-d520-4da5-9c63-1f1c13caea12)

If the comparism returns `True` it calls the `check_pass()` function which validates that we have the right answer
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/5718ac03-d2a3-498d-bb90-365467cb7080)

Else it calls the `check_failed()` function which shows the error message and exits
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/42dba7c6-39f1-476d-a739-7e97c8ab3a53)

So at this point we need the right value that would make `sum == check`

But inorder to do that let's extract the value of the matrix and do some math

The way I got the value is from Ghidra by clicking the matrix variable
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/9753f462-2058-44f4-8512-e5fa4f964eb8)

It looks tricky but to extract it we need to note that one value of the element of the matrix represents 4 bytes remember that the size of an unsigned or signed integer in C is 4 bytes i.e

```
4d 1d 00 00 == 0x1d4d
78 00 00 00 == 0x78
9f 00 00 00 == 0x9f
5d 0b 00 00 == 0xb5d
```

That way after extracting it I got the matrix to be this:

```c
int matrix[4][4] = {
        {0x1d4d, 0x78,  0x9f,  0xb5d},
        {0x149,  0x9cf, 0x130, 0xde8},
        {0x82b,  0x212, 0x596, 0x399},
        {0x9b,   0x983, 0xff,  0x3f2}
}
```

Now that I have the values let's replicate the math done by the program

We represent 4 unknown variables as `x, y, z, t` which should represent the right input

```c
int value[4] = [x, y, z, t];
```

Now the program takes each element of the value array and multiplies it by each element in the matrix where it's sum is saved and used on the next operation

An example representation is this:

```
int matrix [4] = {2, 4, 6, 8};
int x;
int sum;

sum = x*2 + x*4 + x*6 + x*8
```

Looking at the operation gives this:

```
2x + 4x + 6x + 8x
```

From that we know that the common value between each integers is the unknown variable therefore we simplify it to this:

```
x * (2 + 4 + 6 + 8)
```

So this is exactly what we will apply for the matrix in our case it's this:

```
x * {0x1d4d + 0x78 + 0x9f + 0xb5d + 0x149 + 0x9cf + 0x130 + 0xde8 + 0x82b + 0x212 + 0x596 + 0x399 + 0x9b + 0x983 + 0xff + 0x3f2} +
y * {0x1d4d + 0x78 + 0x9f + 0xb5d + 0x149 + 0x9cf + 0x130 + 0xde8 + 0x82b + 0x212 + 0x596 + 0x399 + 0x9b + 0x983 + 0xff + 0x3f2} + 
z * {0x1d4d + 0x78 + 0x9f + 0xb5d + 0x149 + 0x9cf + 0x130 + 0xde8 + 0x82b + 0x212 + 0x596 + 0x399 + 0x9b + 0x983 + 0xff + 0x3f2} + 
t * {0x1d4d + 0x78 + 0x9f + 0xb5d + 0x149 + 0x9cf + 0x130 + 0xde8 + 0x82b + 0x212 + 0x596 + 0x399 + 0x9b + 0x983 + 0xff + 0x3f2}

x * 26220 + y * 26220 + z * 26220 + t * 26220 = 0x00E00C4
```

Looking at the equation we can simplify it to this:

```
26220 * (x + y + z + t) == 0x00E00C4
```

The integer representation of `0x00E00C4` is `917700`

Therefore:

```
x + y + z + t = 917700 / 26220
x + y + z + t = 35
```

We just need to find the value of `x,y,z,t` that when summed gives `35` and as you can tell they are various solutions to this as you might have come up with a valid solution

But for laziness sake I wrote a script that makes use of z3 python library to give the solution

```python
from z3 import *

x, y, z, t = Int('x'), Int('y'), Int('z'), Int('t')

s = Solver()
s.add(x + y + z + t == 35)

if s.check() == sat:
    m = s.model()
    print(f"x = {m[x]}")
    print(f"y = {m[y]}")
    print(f"z = {m[z]}")
    print(f"t = {m[t]}")
```

Running it gives this
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/81c648d2-99c7-48a6-9d4a-aca63e37c250)

```
x = 35
y = 0
z = 0
t = 0
```

So that's one of the solution to the equation and when we feed the binary this input the comparism would return `True`
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/8c5b9ddf-5ec8-4822-b40e-60bfbe465df5)







<h3> Sonda </h3>

A fun reverse engineering challenge ;)

Let's get to it!

We are given a binary and checking the file type shows this
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/9c1e35f9-5975-41a7-936c-5487110b5854)

We're working with a 64bits binary which is dynamically linked and not stripped

I ran it to get an overview of what it does
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/c5acd958-2bf9-4805-8241-d81045407860)

Seems it requires a magic number which i don't know

Let's get on with reversing it which in this case I used IDA

Loading it up in IDA and generating it's pseudocode here's the main function
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/1c68787a-a445-4202-9320-58875db972f6)
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/186735ec-de52-45de-94e9-42ddd1bea1b4)

```c
int __cdecl main(int argc, const char **argv, const char **envp)
{
  size_t v4; // rax
  int v5; // ebx
  unsigned int seed; // [rsp+4h] [rbp-3Ch] BYREF
  int i; // [rsp+8h] [rbp-38h]
  int j; // [rsp+Ch] [rbp-34h]
  int v9; // [rsp+10h] [rbp-30h]
  int k; // [rsp+14h] [rbp-2Ch]
  char *s; // [rsp+18h] [rbp-28h]
  _DWORD *ptr; // [rsp+20h] [rbp-20h]
  unsigned __int64 v13; // [rsp+28h] [rbp-18h]

  v13 = __readfsqword(0x28u);
  printf("Give me the magic number: ");
  __isoc99_scanf("%d", &seed);
  if ( seed % 17 || seed > 20 )
  {
    puts("BAD...");
    return 1;
  }
  else
  {
    s = malloc(seed);
    printf("Tell me more: ");
    __isoc99_scanf("%s", s);
    v4 = strlen(s);
    if ( v4 <= seed )
    {
      srand(seed);
      ptr = malloc(4LL * seed);
      *ptr = 2 * seed + rand() % (5 * seed);
      for ( i = 1; i < seed; ++i )
      {
        v5 = ptr[i - 1];
        ptr[i] = v5 + rand() % 94 + 33;
      }
      for ( j = 0; j < seed; ++j )
      {
        v9 = 0;
        for ( k = 0; k <= j; ++k )
          v9 += s[k];
        if ( v9 != ptr[j] )
        {
          puts("NOOB! Keep trying...");
          free(s);
          free(ptr);
          return 1;
        }
      }
      printf("flag\n");
      free(s);
      return 0;
    }
    else
    {
      puts("WTF is wrong with u?");
      free(s);
      return 1;
    }
  }
}
```

Here's what the code does:

First portion:

```c
  printf("Give me the magic number: ");
  __isoc99_scanf("%d", &seed);
  if ( seed % 17 || seed > 20 )
  {
    puts("BAD...");
    return 1;
  }
```

- First it receives a number which is the "magic number" which is stored as `seed`, and checks if it's divisible by 17 or greater than 20.
  - If it is, then the program just returns 1 and basically stop it's execution.

In order to pass this check we need to pass a number which is divisible by 17 and less than 20. The only numbers which meet that check are 0 and 17.

```
seed = [0, 17]
```

Second portion:

```c
s = malloc(seed);
printf("Tell me more: ");
__isoc99_scanf("%s", s);
v4 = strlen(s);
if ( v4 <= seed )
{
  srand(seed);
  ptr = malloc(4LL * seed);
  *ptr = 2 * seed + rand() % (5 * seed);
  for ( i = 1; i < seed; ++i )
  {
    v5 = ptr[i - 1];
    ptr[i] = v5 + rand() % 94 + 33;
  }
```

- It allocates dynamic memory with the size of the magic number
- Receives our input which is then stored in the malloc'd pointer `s`
- Checks if the length of the input is less than or equal to the seed (magic number)
  - If the length isn't equal it would stop it's execution after giving the error message "WTF is wrong with u?"
- If the input length matches the check then it does this:
  - Calls `srand()` seeding it with the magic number
  - Allocates dynamic memory with size of `(4 * seed)` which is stored in pointer `ptr`
  - Sets `ptr[0]` to `2 * seed + rand() % (5 * seed);`
  - In a for loop with range of `1-17` it sets an integer `v5` which is the value gotten from `ptr[i-1]` and then each index of the malloc'd pointer is set to `v5 + rand() % 94 + 33`

For this portion we know that since it seeds srand with the magic number which is 17 that means we can also generate the list of 17 random integers it creates

The reason the magic number can't be 0 is because it generates some value in the malloc'd pointer and we can loop over a value that's 0

Third portion:

```c
for ( j = 0; j < seed; ++j )
{
  v9 = 0;
  for ( k = 0; k <= j; ++k )
    v9 += s[k];
  if ( v9 != ptr[j] )
  {
    puts("NOOB! Keep trying...");
    free(s);
    free(ptr);
    return 1;
  }
}
printf("flag{%s}\n", s);
free(s);
return 0;
}
```

- Looping over the range of the seed (0, 17) as (j)
- It sets variable `v9` to 0
- In a nested loop ranging from `0 to (j)`, it get's the sum of our input from the two current nested loop index
- And after the inner loop is completed it checks if the generated sum equals `ptr[j]`
- If it is that means our input is the flag else we get the error message "NOOB! Keep trying..."

The algorithm here is pretty tricky relative to me.

At this point we know that the flag length is the same as the seed i.e 17

How do we get the flag?

To solve this I made use of an [SMT](https://en.wikipedia.org/wiki/Satisfiability_modulo_theories) solver called [Z3](https://github.com/Z3Prover/z3)

First we need to generate the 17 various random value gotten when seeded with 17

I wrote a simple C program for that

```c
#include <stdio.h>

int main(void){
    unsigned int seed = 17;
    srand(seed);

    for (int i = 0; i < seed; i++){
        printf("%d\n", rand());
    }
}
```

Running it generates the value
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/80143ca5-c4fb-4654-8d34-2faf1f4f31f9)

And now I stored them in a list

```
rands = [1227918265, 3978157, 263514239, 1969574147, 1833982879, 488658959, 231688945, 1043863911, 1421669753, 1942003127, 1343955001, 461983965, 602354579, 726141576, 1746455982, 1641023978, 1153484208]
```

Now here's my final script

```python
from z3 import *

rands = [1227918265, 3978157, 263514239, 1969574147, 1833982879, 488658959, 231688945, 1043863911, 1421669753, 1942003127, 1343955001, 461983965, 602354579, 726141576, 1746455982, 1641023978, 1153484208]
seed = 17

ptr = [BitVec(f"seed_{i}", 32) for i in range(seed)]
flag = [BitVec(f"f_{i}", 8) for i in range(seed)]

s = Solver()

s.add(ptr[0] == 2 * seed + rands[0] % (5 * seed))

for i in range(1, seed):
    v5 = ptr[i-1]
    s.add(ptr[i] == v5 + rands[i] % 94 + 33)

for j in range(0, seed):
    v9 = BitVecVal(0, 32)
    for k in range(0, j+1):
        v9 += ZeroExt(24, flag[k])
    
    s.add(ptr[j] == v9)

if s.check() == sat:
    m = s.model()
    print(m)
```

Running it generates the right value
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/1d46113b-c4e7-4bb8-884a-8dec7247bb75)

I then saved the `f_*` values in a list and got it's equivalent character presentation

```python
soln = [89, 117, 123, 69, 74, 36, 92, 102, 62, 54, 34, 86, 48, 76, 124, 110, 54][::-1]
print(''.join(list(map(chr, soln))))
```

Running it generates this
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/4c05fe26-05aa-4a52-b01c-aca41cb090fa)

Trying that as the flag worked!
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/c32aa1f5-188e-4978-a3bc-75a60633981f)

```
PS C:\Sonda> python .\solve.py
6n|L0V"6>f\$JE{uY
```

And that's all!

Thanks for reading 😅

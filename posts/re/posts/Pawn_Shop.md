<h3> Flag Appraisal (MetaCTF July 2024) </h3>

So today I participated in the MetaCTF Monthly Challenge

And i'll be showing you how I solved the Reverse Engineering challenge called `Flag Appraisal`

![image](https://github.com/user-attachments/assets/84925ab1-e5a8-4afc-8170-ee3c8ffe0b53)

I actually never got to submit the flag because I ended up solving it 3 minutes after the ctf ended due to skill issue and one thing is that the ctf runs for just 2 hours

So less talking and let's get to the main thing

We are given a x64 executable called `pawn_shop`
![image](https://github.com/user-attachments/assets/d05a6885-6700-4192-94f3-abc1462e4e38)

The binary is also stripped so that means we won't have function name 

I ran the binary to get an overview of what it does
![image](https://github.com/user-attachments/assets/ed3a1f37-d643-45ed-aab6-1c4925dc4dcd)

It looks like we need to give it the right input to solve this and the input is going to be the flag?

Time for some static analysis

Using Ghidra I decompiled the binary

Here's the entry function

![image](https://github.com/user-attachments/assets/e3d81089-dcda-4b4e-9e1c-334b15ffc60a)

```

void processEntry entry(undefined8 param_1,undefined8 param_2)

{
  undefined auStack_8 [8];
  
  __libc_start_main(FUN_0010128e,param_2,&stack0x00000008,0,0,param_1,auStack_8);
  do {
                    /* WARNING: Do nothing block with infinite loop */
  } while( true );
}
```

The first parameter passed into `__libc_start_main` is the `main` function so i renamed it
![image](https://github.com/user-attachments/assets/78f82e66-ab68-4f58-8010-4eacf1d7b9a4)

Moving on, we can check the main function decompilation and we should get this
![image](https://github.com/user-attachments/assets/2ba95576-97ff-41ab-bb20-75807e848fa3)

The decompilation is pretty understandable but still i prefer to rename my variable cause it's way more better
![image](https://github.com/user-attachments/assets/a62c0a12-4450-4dbc-a946-9bf861af73bc)

```c

bool main(void)

{
  int fp;
  size_t n;
  long in_FS_OFFSET;
  char flag [104];
  long canary;
  
  canary = *(long *)(in_FS_OFFSET + 0x28);
  printf("Welcome to my Pawn Shop, go ahead and show me the flag you want appraised: ");
  fgets(flag,100,stdin);
  n = strcspn(flag,"\n");
  flag[n] = '\0';
  n = strlen(flag);
  mangle(flag,n & 0xffffffff);
  fp = strncmp(flag,&enc_flag,0x25);
  if (fp != 0) {
    puts("Unfortunately, your flag here looks to be a counterfeit.");
  }
  else {
    puts("Well good news, your flag looks to be authentic! Best I can do is $2.");
  }
  if (canary != *(long *)(in_FS_OFFSET + 0x28)) {
                    /* WARNING: Subroutine does not return */
    __stack_chk_fail();
  }
  return fp != 0;
}
```

From this we can see it would
- Receive our input and store it in variable `flag`
- Remove any new line character (basically null terminating our input)
- Gets the length of our input which is stored in variable `n`
- Calls function `mangle()` passing our input and the length as the parameter
- Compares our mangeld input with the encrypted flag
- If the comparism if right that means we got the right flag input else we didn't get it

From this we can conclude that our flag length should be 37 and the input we give it is going to be mangled before being compared against the encrypted flag

Let's check the mangle function
![image](https://github.com/user-attachments/assets/85ddf378-c532-438f-be64-cfbe0ab28804)

Not bad but I had to rename variables and change the data types and i got this
![image](https://github.com/user-attachments/assets/d3b6a4e3-2ed2-4e4f-85f0-02f3d3b97252)

The C decompilation without type casting should look like this:

```c

void mangle(char *flag,uint length)

{
  uint state;
  int i;
  
  state = 0;
  for (i = 0; i < (int)(length - 1); i = i + 2) {
    state = state * 0x21 ^ flag[i + 1] * 0x1fd ^ flag[i] * 0x101;
    flag[i] = state;
    flag[i + 1] = (state >> 8);
  }
  if ((length & 1) != 0) {
    flag[length + -1] = state * 0x21 ^ flag[length + -1];
  }
  return;
}
```

So what does this do?

- It initializes variable `state` to 0
- First it interates through the length of our input minus one then incrementing the iterate by 2. For each iteration it does this
    - Generate a new state based on the current flag character and the succeeding one using xor and multiplication
    - Sets the current flag value to the generated state
    - Bit right shift the state value by 8 and sets the succeeding flag value to it
- If the length of the flag provided is not divisible by 2 then it sets the last character to a certain value based on the xoring the current state value with the character and 33


That's how the mangling algorithm is

So after this mangling is done it compares the mangled input with this:

```
enc = [ 0x9c, 0x85, 0xb5, 0x8d, 0x12, 0xa0, 0x9b, 0x10, 0xe8, 0x1f, 0x2b, 0xb3, 0xdb, 0x4a, 0x87, 0x1e, 0x39, 0xbd, 0x03, 0x32, 0xc6, 0xd0, 0x82, 0xdb, 0xcd, 0x46, 0x82, 0xa1, 0x6d, 0x09, 0x80, 0xe5, 0x6c, 0x7f, 0x6c, 0x82, 0x91 ]
```

Now how did I go about solving it?

At first, I was too lazy to reverse it, so I tried to brute force the right character. However, the issue was that the current character depends on the next character, which means having to brute force two characters at a time.

That kind of worked, but it gave so many values that met the condition. So that would mean I needed to figure out the right word that made (sense / readable) for every values gotten

That is pretty stressful so I gave up on that idea

After about an hour spent coming up with that I decided to actually reverse it and solve it a better way

This is basically the algorithm and one thing i noticed was this:

```c
state = 0

state = (state * 33) ^ (flag[i + 1] * 509 ^ (flag[i] * 257)
flag[i] = state
flag[i + 1] = state >> 8
```

We can reverse the last step by doing this

```c
flag[i + 1] = state << 8
```

But then the value won't be 100% accurate

You might be thinking what do i mean by that

Bitwise left and right shifts are not inverse operations and serve different purposes: left shifting increases the value (similar to multiplication by powers of 2), while right shifting decreases the value (similar to division by powers of 2).

One way to just know this is by trying to play with it using different value and see for yourself

Ok back to the challenge how do we ensure that the state value we get is actually right?

Because we know that the flag starts from `MetaCTF` we can use the first two character to generate the next state value

And we can then apply a smart brute force technique

Since we know the current state for the iteration:

```
state = (state * 33) ^ (flag[i + 1] * 509 ^ (flag[i] * 257)
```

We can brute force for `flag[i] & flag[i + 1]` and we pass the two values into the mangling algorithm then we compare the mangled value against the encrypted value

If it's right that means we've retrieved it and we can as well use that to generate the next state value and the next two characters

This process is going to be repeated till we get to `len(flag) - 1`

Here's my solve script

```python
import string

def get_key(v1, v2):
    value = v2 << 8
    for i in range(value, value+1000):
        op1 = i & 0xff
        op2 = (i >> 8) & 0xff
        if (op1 == v1) and (op2 == v2):
            value = i

    return value

def brute(value):
    charset = string.ascii_letters + '{_}'
    for var1 in charset:
        for var2 in charset:
            op = (257 * ord(var1)) ^ (509 * ord(var2))
            if op == value:
                return var1 + var2

def mysolve(var1, var2, key):
    charset = string.printable 

    for v1 in charset:
        for v2 in charset:
            value = (257 * ord(v1)) ^ (509 * ord(v2)) ^ (33 * key)
            cmp1 = value & 0xff
            cmp2 = (value >> 8) & 0xff

            if (cmp1 == var1) and (cmp2 == var2):
                return (v1, v2, value)


enc = [ 0x9c, 0x85, 0xb5, 0x8d, 0x12, 0xa0, 0x9b, 0x10, 0xe8, 0x1f, 0x2b, 0xb3, 0xdb, 0x4a, 0x87, 0x1e, 0x39, 0xbd, 0x03, 0x32, 0xc6, 0xd0, 0x82, 0xdb, 0xcd, 0x46, 0x82, 0xa1, 0x6d, 0x09, 0x80, 0xe5, 0x6c, 0x7f, 0x6c, 0x82, 0x91 ]
flag = ""

key = get_key(enc[0], enc[1])
flag += brute(key)


for i in range(2, len(enc)-1, 2):
    v1 = enc[i]
    v2 = enc[i+1]
    r = mysolve(v1, v2, key)
    flag += r[0] + r[1]
    key = r[2]
    
flag += '}'

print(flag)
```

Running it gives the flag
![image](https://github.com/user-attachments/assets/ea603a3c-4ac5-45ea-86aa-efe1593263fd)

```
Flag: MetaCTF{c0un73rf3171ng_7h3_p4wn_$h0p}
```

Sayonara 😃








































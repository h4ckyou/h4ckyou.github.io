<h3> Urchinsec XMAS 2023 CTF </h3>

![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/1f0815f9-8bb1-4c87-b612-69c1107d0b7d)

#### INITIAL DETAILS 
I wanted to make a detailed solution.......... but eventually felt lazy to do so

So you can view the solve script of some challenges: [link](https://github.com/h4ckyou/h4ckyou.github.io/blob/main/posts/ctf/urchinsec23/)

#### FINAL DETAILS

The organizers put a prize on the best writeup that would be provided then I came back here to make a detailed writeup! 😸
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/9bb0ac0c-75a0-4ec9-af40-f11731fce45f)

I will be writing on the crypto, pwn and rev challenges that I solved.

#### Reverse Engineering
- Sexy Primes
- UrchinFlag
- SugarPlum

#### Cryptography
- Minstix
- SantaZIP
- Honey Sea
- By Polar RSA

#### Pwn
- BOF

### Reverse Engineering

#### Sexy Primes
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/de1ea3d1-5038-47b5-b4ac-6bfd76fac54b)

So we're working with a x64 binary which is dynamically linked and not stripped

Running it keeps printing out `6` for some reason

Decompiling it in Ghidra and going over to the main function shows this
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/21b121cb-880e-4edf-8707-537536dfbd1e)

```c
undefined8 main(void)

{
  sexyprime();
  return 0;
}
```

Nothing really there except that it calls the `sexyprime` function

Here's the decompiled `sexyprime` function
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/4918dd40-aede-41e4-a019-a9664fdeee65)

```c
void sexyprime(void)

{
  long in_FS_OFFSET;
  long canary;
  
  canary = *(long *)(in_FS_OFFSET + 0x28);
  printf("%d",6);
  if (canary != *(long *)(in_FS_OFFSET + 0x28)) {
                    /* WARNING: Subroutine does not return */
    __stack_chk_fail();
  }
  return;
}
```

Looking at it we can see it just indeeds prints out `6` but is that all?

Ghidra does not seem to decompile the binary well I have no idea why, but if you take a look at the assembly decompilation you'd see it does some other stuffs
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/6a146c4f-af52-441d-86d9-78a6c99f0ffb)

At some point it's supposed to receive user input but that check isn't being reached

So I decided to manually step through each instruction to figure why it doesn't work

I set a breapoint at the `sexyprime` function:

```
break *sexyprime
```

At `sexyprime+58` I saw that it compares the value of `$rbp-0x80` to `0x6`, checking the current value shows it's right
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/390db2f2-9c3b-4402-8431-374f484a018a)

Moving to the next 3 instructions shows another comparism
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/11da310c-8758-481a-882b-c40b250f57b5)

The reason it would fail is because of this:

```
mov    DWORD PTR [rbp-0x7c], 0x10
```

The value of `$rbp-0x7c` would be `0x10` and when it's compared to `0x6` that would return False

In this case it would fail and if it does it would jump to `sexyprime+1701` which would `ret` and the program would exit

























I played as `@rizz` 🙂

![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/aa3e5b95-6373-493f-9ce9-c69069021017)

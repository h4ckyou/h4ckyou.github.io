<h3> Perfectroot CTF 2024 </h3>

![image](https://github.com/user-attachments/assets/b55b9b6d-8b2c-429a-bd9f-b2542a787953)

Hey guys, 0x1337 here! Over the weekend I participated in this CTF with team `One Piece`

We ended up placing first so GGs to my team mates and every one
![image](https://github.com/user-attachments/assets/b15e30fe-d482-45c8-bd19-28aa3aad45a9)

I played as `ptr` btw
![image](https://github.com/user-attachments/assets/370d8198-f5fe-4c1a-ae6b-d950b1eff119)

I'm making this writeup because of the writeup contest lmao (i'm too tired to make it though)
![image](https://github.com/user-attachments/assets/6d9a5a42-50bc-4801-9c6c-94eae78b55a3)

Anyways I don't plan on making the solutions to all the challenges I solved but rather Pwn, Rev and Web
![image](https://github.com/user-attachments/assets/df755a22-23e7-4252-9e9e-b56a2228e82b)
![image](https://github.com/user-attachments/assets/cefac533-589c-4c64-b5de-707fc900547b)
![image](https://github.com/user-attachments/assets/6d01822d-971d-47d7-8673-fcbf0047cefc)

## Pwn
- Flow
- Nihil
- Daily Routine
- Heap Wars
- Heaps Don't Lie
- Sea Shells
- Arm and a Leg

## Rev
- Hackers Catch
- Re-Incarnation
- Hackers Catch 2
- Go Dark
- Box
- Pores

## Web
- Console-idation


### Pwn 7/8 :~

#### Flow
![image](https://github.com/user-attachments/assets/5fb6d5b0-074f-4859-bce8-c3a44eb5ddfb)

I downloaded the attached file and checking the file type shows this
![image](https://github.com/user-attachments/assets/a919c171-5503-44fa-a3dd-903e5eea7334)

So we're working with a 64bits executable which is dynamically linked and not stripped

From the protections shown by `checksec` we can see just `PIE and NX` enabled

Moving on, I ran the binary to get an overview of what it does
![image](https://github.com/user-attachments/assets/f618f612-f8a3-46ab-bd9b-14560fff5a3e)

It seems to receive our input then the program stops!

Okay time to reverse it, throwing it into IDA i get the main function
![image](https://github.com/user-attachments/assets/906e2ed7-f639-4366-8039-6d94c3aa6a63)

The main function just calls the `vulnerable` function, and here's the decompilation
![image](https://github.com/user-attachments/assets/ee2170fb-2efc-4cc7-8a16-012eaa349169)

```c
__int64 vulnerable()
{
  __int64 result; // rax
  _BYTE v1[60]; // [rsp+0h] [rbp-40h] BYREF
  int v2; // [rsp+3Ch] [rbp-4h]

  v2 = 12;
  printf("Enter a text please: ");
  result = __isoc99_scanf("%64s", v1);
  if ( v2 == 0x34333231 )
    return win();
  return result;
}
```

Okay looking at the pseudocode, we can see that:
- it defines a char array `v1` that can hold up 60 bytes of data
- a variable `v2` is initialized to 12
- after it receives our input which is then stored into `v1` it does a comparism that checks if `v2` equals `0x34333231`
- if the comparism returns True it calls the win function which basically prints the flag else it just returns

![image](https://github.com/user-attachments/assets/e6ad10a9-1703-4202-8f0d-6024b45d64dc)

Ok firstly the vulnerability is a 4 byte overflow and the reason is due to the program reading in at most 64 bytes into a buffer that can only hold up 60 bytes 

Our goal is to overwrite the v2 variable to the expected value because that check can never pass since v2 is initialized as 12

Looking at the stack view of the function we get this
![image](https://github.com/user-attachments/assets/009c5371-d5b6-4918-aa9a-c88d0d6b1e7d)

Basically after the buffer is the v2 variable, so this means if we fill up the buffer with 60 bytes the next 4 bytes will overwrite the check (v2) variable

So here's our goal:
- Fill up the buffer with junk 60 bytes
- Overwrite the v2 variable with 0x34333231
- Profit

Doing that i get the flag and here's my [solve](https://github.com/h4ckyou/h4ckyou.github.io/blob/main/posts/ctf/perfectr00t24/scripts/Flow/solve.py)
![image](https://github.com/user-attachments/assets/bab0e779-c119-4d26-a361-c8fdb6818cdf)

```
Flag: r00t{fl0w_0f_c0ntr0l_3ngag3d_7391}
```

#### Nihil
![image](https://github.com/user-attachments/assets/9111315d-a14d-49eb-ac0d-fcd911e44099)

I downloaded the attached file and checking the file type shows this
![image](https://github.com/user-attachments/assets/031846f2-fbef-423f-a16b-7397d77c5079)

Pretty much same as before so i'm not repeating myself

I ran the binary to get an overview of what it does
![image](https://github.com/user-attachments/assets/d70d13a1-10cd-4bd0-a8c3-1a6a0bec277f)

Running it, we can see that it receives a number and a string before exiting 

Loading it in IDA here's the main function
![image](https://github.com/user-attachments/assets/ba731bb2-55a1-4405-b857-ac16e60b6407)

```c
int __fastcall main(int argc, const char **argv, const char **envp)
{
  char s[16]; // [rsp+0h] [rbp-20h] BYREF
  unsigned __int64 v5; // [rsp+10h] [rbp-10h]
  unsigned int v6; // [rsp+1Ch] [rbp-4h]

  setbuf(stdin, 0LL);
  setbuf(_bss_start, 0LL);
  printf("How much did you get? ");
  fgets(s, 100, stdin);
  v6 = atoi(s);
  v5 = v6 + 1;
  puts("Any last words?");
  fgets(s, 100, stdin);
  if ( v5 < v6 )
  {
    printf("What, How did you beat me?");
    if ( v6 == 727 )
    {
      printf("Here is your flag: ");
      flag_file = fopen("flag.txt", "r");
      fgets(flag, 100, flag_file);
      puts(flag);
    }
    else
    {
      puts("Just kidding!");
    }
  }
  else
  {
    printf("Ha! I got %d\n", v5);
    puts("Maybe you will beat me next time");
  }
  return 0;
}
```

Let's understand what this does:
- first it reads in our input into variable `s`
- it then converts the string in `s` to an integer and stores the resulting int value into `v6`
- it sets `v5` to the `v6 + 1`
- receives our input again into variable `s`
- if the `v5` variable is less than `v6` it will compare the v6 with 727 and it's equal we get the flag else some error message

At first it might look like we just need to set our first input to 727 such that when it's converted we would pass the check

But that won't work because if we do that then v5 is set to `727 + 1 = 728` and the check done on `v5` to make sure it's less than `v6` won't return true because at that point v5 > v6 thereby giving us the error message

Now what's the bug? Well there's a buffer overflow on both the first & second read

It defines a char buffer `s` which can hold up at most `16` bytes of data, but during our read we actually `fgets` at most `100` bytes into the `s` buffer leading to an overflow

What can we do with this? 

Our goal is obviously to pass the check because doing that would give us the flag

Here's what i did

Notice how we have the overflow on our second read and basically at that point the v5 & v6 variables would already hold some value and there are going to be on the stack and we are still reading into the `s` variable

Now take a look at the stack of the function
![image](https://github.com/user-attachments/assets/6764f11d-0d3d-4196-a873-6b804cd95073)

Basically we can groom the stack such that we leverage the overflow and set those varaibles to any value we want

This is how my payload looks like:
- junk to just set v5 to a value (in order to reach second read)
- fill up the s variable with 16 bytes -> the next 8 bytes is the v5 variable so we overwrite that with a small value -> padding with 4 bytes -> next 4 bytes is the v6 variable and we set that to the expected value 727

Doing that should give us the flag and here's my [solve]()
![image](https://github.com/user-attachments/assets/3f362af2-c4c4-440a-8aa3-7b68f737b07f)

```
Flag: r00t{n0th1ng_t0_h1d3_wh3n_th3_fl0w_1s_nihil_9027}
```





















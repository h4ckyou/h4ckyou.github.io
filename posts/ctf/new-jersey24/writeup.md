### New Jersey 2024 CTF

#### It was fun and I only focused on solving the Binary Exploitation & Reverse Engineering challenges. I played with `THE TOMATO DUDES`
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/e465014d-57ac-44c0-957e-7adf914b3089)

Currently the scoreboard is hidden though the ctf is over so i can't see our position nor each user point

#### Challenges Solved:
  - Humble Beginnings (reverse)
  - Password Manager (reverse)
  - Searching-Through-Vines (pwn)
  - Math Test (reverse)
  - The Heist 1 (reverse)
  - Running On Prayers (pwn)
  - Stage Left (pwn)
  - Postage (pwn)
  - The Heist 2 (reverse)

Out of this I was able to do 8/9 from this category
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/23b098bb-9f86-409b-8dee-1f9d7cb18f4e)

So let's start...

##### Humble Beginning
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/1d690764-40c6-41a8-9eaa-09e1aff297de)

So our goal is to find the crypto wallet address

After downloading the executable I loaded it up in IDA and generated the pseudocode

Here's the main function
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/7f1e3de0-234a-4349-8f65-0c6bb73a818c)

At this line:

```c
sub_140001010(v4, "mxnhCEkuBogW3E7XAEzNmaq6eZqW3zgEuu");
```

It's calling function `sub_140001010` passing `v4` which is the first argument we pass to the executable as the first parameter and some weird string as the second parameter

Using that as the address worked

```
Flag: jctf{mxnhCEkuBogW3E7XAEzNmaq6eZqW3zgEuu}
```

#### The Heist 1
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/81d4932d-2357-45b5-8d72-20ce06ca3ead)

So this time around our goal is to find the pin

I downloaded the executable, loaded it up in IDA and generated the pseudocode

Here's the main function
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/0a15821d-5221-4b07-8809-86eff4536dde)

```c
int __fastcall main(int argc, const char **argv, const char **envp)
{
  FILE *v3; // rax
  char v4; // al
  char *i; // rcx
  char *v6; // rcx
  char Buffer[16]; // [rsp+20h] [rbp-88h] BYREF
  __int128 v9; // [rsp+30h] [rbp-78h]
  __int128 v10; // [rsp+40h] [rbp-68h]
  __int128 v11; // [rsp+50h] [rbp-58h]
  __int128 v12; // [rsp+60h] [rbp-48h]
  __int128 v13; // [rsp+70h] [rbp-38h]
  int v14; // [rsp+80h] [rbp-28h]

  sub_140001010("Please enter the pin:");
  v14 = 0;
  *(_OWORD *)Buffer = 0LL;
  v9 = 0LL;
  v10 = 0LL;
  v11 = 0LL;
  v12 = 0LL;
  v13 = 0LL;
  v3 = _acrt_iob_func(0);
  if ( fgets(Buffer, 100, v3) == Buffer )
  {
    v4 = Buffer[0];
    for ( i = Buffer; *i; v4 = *i )
      *i++ = __ROL1__(~(v4 + 96), 4) ^ 0x55;
    if ( qword_140003038 != *(_QWORD *)Buffer || (v6 = "Success", dword_140003040 != *(_DWORD *)&Buffer[8]) )
      v6 = "Failure";
    sub_140001010(v6);
  }
  return 0;
}
```

The function `sub_140001010` just prints out the word passed as the parameter
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/88a61295-b18d-4192-afc6-ee23819a0c30)

So let's see what it does:
- It would receive our input using `fgets` which is stored in the `Buffer` char array
- Then for each value in the array it does this:
  - It adds `96` to the value
  - Negates the result
  - Rotates the result `4` times to the left
  - Xors the rotated value with `0x55`
- After the encryption is done it will then:
  - Compare the resulting value to what's stored in `qword_140003038`
  - Compares the `Buffer[8::]` to the value stored in `dword_140003040`
- If the comparism returns `True` we get the success message else the failed message

Looking at the value stored in `qword_140003038` shows
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/b4bb83ba-919a-46fb-a6ce-956789ad1866)

```
qword_140003038 = 0xE383C3B3232383C3
dword_140003040 = 0xC33E3A3
```

That's basically the encrypted pin value

So our goal is to reverse the operation to find the right value to get us that?



![image](https://github.com/user-attachments/assets/836f038f-67da-4591-9ba7-f84005399c43)<h3> Battle CTF 2024 </h3>

![image](https://github.com/user-attachments/assets/9d74fbd3-a76b-421c-8247-8630551c826d)

Hii 0x1337 here, this writeup contains the challenges I was able to solve in the Battle CTF 2024 prequalifiers event!

Hope you have fun reading.

Challenges:
- Rules (Misc)
- Invite Code (Misc)
- Do[ro x2] (Forensics)
- Sweet Game (Pwn)
- Universe (Pwn)
- NTCrack (Pwn)
- 0xterminal (Pwn)
- Hmmmm!... (Web)


**Rules**

Going over to the discord channel and checking the #announcement page gives the flag
![image](https://github.com/user-attachments/assets/8ec1e651-47c2-4989-972d-b314bb4801d1)

```
Flag: battleCTF{HereWeGo}
```

**Invite Code**

This challenge was actually released prior to the ctf beginning and you can find it on the discord here
![image](https://github.com/user-attachments/assets/1da6c398-493c-462b-933d-e2758158e7bb)

After decoding from hex it gives this
![image](https://github.com/user-attachments/assets/ab4af42a-ec7c-4093-b78f-cb8f9432e720)

```
UWNYZ1c5dzR3UWQvZWIudXR1b3kvLzpzcHR0aA=https://bugpwn.com/invite.ini
```

There are two things of interest there, one is a base64 encoded value and the other is the invite link path?

Spoiler alert:- The base64 value decodes to a Youtube link which rickrolls you :)

On checking the invite link i got this
![image](https://github.com/user-attachments/assets/64220696-88d8-4479-87c2-0bdd8fd2f6fd)

```
H4sIAKvQ/2YC/02TW08bQQyFn+FXHCKk9iXN3C9SEjS7MytVlIsAqUKKVC1JgJRk0yahTf997VC1fUBMduzj48+eh3eTfTud7OezyV4I+rO795N90MOz/WqJH/PNdrHuRj35QfQw76br2aJ7GvVed4/90MN213azdrnu5qNet+7hbHw8PMlX9d39dcHrlpJxe397Vy5AF2+/V+1+1AuyNz4+Onyhm6Oj4XL9tOi6djUfP7S73XI+3T0OB/8+csi3drv9ud7MxqeqPZXqdD59Xcjl3eri8/nNxY35OjPm5fHq5XoflvP2k9id18/d5WJmlpfp4XkzuH++vt5/Hw7+yrCmmW6+UFObX992Y2FhGygHbxArhIzsISJMRKngJKKBzRAePkNqpIQS4C3qDJcgC3yEVMiHc6BbD9WwZiY1j2IgSFNxLp2DQimQAqlG8tAJFQUbVArJIFloh5KgakgHIRAiUkEVoBREhcZCBtQJQkMr1HR2cBVsQBAoNbyA93CF020N67iia5Ayp9cWkW6ptciapnDpKBAtqgomo2T2HCNiYGMkmA2K4r6oC0r3jkuzKwcpkSp4DeeRBDMhq7pGoHYcQ1OSg73kWjlyjCakZFvAVn+gkckouaiMcBriwIHCBBkjA4Kdk7ImZWKu0VAi9VtQEw3SSYwxVMjNARcdyADhItsNGsO068JVSLPRUILh1wpWcYr1PBobWZBKGIdMIpZjuMeaN4FGT1LUOw8u83Dpig5Bw0rmT1I68HxV4nQq4Wgomb9XtD+aDTMKd+jIss/KMzoteMcItW+4HZqg9LwANDuqSGBpKOTNCd4cc+iXBlFlNA2bTBLaM2eaIyEljFGhoXEHdss2AjNnPsShGg7+33t6hwN+iPRCD/+348lm0g1P+n28vcX6jramuflIy6YE4ez3DxG/AVECNBs5BAAA
```

Decoding it gave this
![image](https://github.com/user-attachments/assets/9224adcf-8fe7-45e4-bce4-b15f9147f49e)

The decoded value is a compressed archive (gzip)

I extracted it
![image](https://github.com/user-attachments/assets/b532ecbf-5d6b-4816-b1b3-e0d5e000a269)

The content is an XML file

```xml
<?xml version="1.0" encoding="utf-8" standalone="no" ?>
<!DOCTYPE users SYSTEM >
<users max="81">
        <user >
                <loginname>battlectf</loginname>
                <password>$2a$12$ecui1lTmMWKRMR4jd44kfOkPx8leaL0tKChnNid4lNAbhr/YhPPxq</password>
                <4cr_encrypt>05 5F 26 74 9B 8D D7 09 49 EB 61 94 5D 07 7D 13 AA E8 75 CD 6A 1E 79 12 DA 1E 8A E7 2F 5F DB 87 E4 0D D2 13 E4 82 EE 10 AC A7 3A BF 54 B2 A4 A5 36 EA 2C 16 00 89 AE B8 22 0B F5 18 CA 03 32 C8 C6 6B 58 80 EC 70 77 6E 16 5C 56 82 6F AD 0B C5 97 69 E9 B8 4E 54 90 95 BB 4D ED 87 99 98 BF EC D4 E2 8A 0D C5 76 03 89 A6 11 AB 73 67 A0 75 AE 3C 84 B6 5D 21 03 71 B8 D9 A0 3B 62 C0 5B 12 DA 5C 91 87 19 63 02 A4 3B 04 9F E0 AD 75 3E 35 C3 FB 1B 5E CB F0 5A A7 8B DF 00 8B DC 88 24 EF F4 EE CE 5C 3B F3 20 10 C2 52 DF 57 D2 59 5E 3E 46 D0 85 10 89 AC 09 07 EF C5 EE 1D 2F 89 1D 83 51 C6 52 38 13 2A D0 20 66 6D 52 B1 93 1B 21 06 9F E5 00 B7 AB 30 EB 98 7F CB 80 17 36 16 EF 73 BB 59 60 E4 4B F0 8A BD FF 85 A1 37 5D 4E C0 91 92 F2 68 C5 20 68 A0 A7 84 EB</4cr_encrypt>
        </user>
</users>\r\n<!-- battleCTF AFRICA 2024 -->\r\n 
```

From the xml content we can see there are 3 fields:
- loginname
- password
- 4cr_encrypt

The last one looks oddly like `rc4_encrypt` so we can assume that we need to rc4 decrypt that hex value, but that requires the key 

Since there's also a password hash we can assume that the rc4 key is the password plaintext value

From this I used JTR to crack the hash and that took time but yea it cracks!
![image](https://github.com/user-attachments/assets/98d209a4-6f0f-4993-9bda-0cd398727621)

The password is `nohara`

At this point I just looked for a rc4 decrypt implementation in python and got [this](https://pycryptodome.readthedocs.io/en/latest/src/cipher/arc4.html)

So we just need to call the `ARC4` class with the password and use the `decrypt` function

Doing that I got the decoded message
![image](https://github.com/user-attachments/assets/45fd9d00-6ebf-4707-8da3-3bdde78de3a7)

```python
from arc4 import ARC4

password = "nohara".encode()
arc4 = ARC4(password)
ct = bytes.fromhex("05 5F 26 74 9B 8D D7 09 49 EB 61 94 5D 07 7D 13 AA E8 75 CD 6A 1E 79 12 DA 1E 8A E7 2F 5F DB 87 E4 0D D2 13 E4 82 EE 10 AC A7 3A BF 54 B2 A4 A5 36 EA 2C 16 00 89 AE B8 22 0B F5 18 CA 03 32 C8 C6 6B 58 80 EC 70 77 6E 16 5C 56 82 6F AD 0B C5 97 69 E9 B8 4E 54 90 95 BB 4D ED 87 99 98 BF EC D4 E2 8A 0D C5 76 03 89 A6 11 AB 73 67 A0 75 AE 3C 84 B6 5D 21 03 71 B8 D9 A0 3B 62 C0 5B 12 DA 5C 91 87 19 63 02 A4 3B 04 9F E0 AD 75 3E 35 C3 FB 1B 5E CB F0 5A A7 8B DF 00 8B DC 88 24 EF F4 EE CE 5C 3B F3 20 10 C2 52 DF 57 D2 59 5E 3E 46 D0 85 10 89 AC 09 07 EF C5 EE 1D 2F 89 1D 83 51 C6 52 38 13 2A D0 20 66 6D 52 B1 93 1B 21 06 9F E5 00 B7 AB 30 EB 98 7F CB 80 17 36 16 EF 73 BB 59 60 E4 4B F0 8A BD FF 85 A1 37 5D 4E C0 91 92 F2 68 C5 20 68 A0 A7 84 EB")

print(arc4.decrypt(ct).decode())
```

And we have the flag!

```
Flag: battleCTF{pwn2live_d7c51d9effacfe021fa0246e031c63e9116d8366875555771349d96c2cf0a60b}
```

**Do[ro x2]**

This is the solution in pdf format: [solution](https://github.com/h4ckyou/h4ckyou.github.io/blob/main/posts/ctf/battlectf24/Dororo/Dororo.pdf)

**Sweet Game**

We are given an executable, and checking the file type and protections enabled on it shows this
![image](https://github.com/user-attachments/assets/3abfd42e-c882-4715-9f41-bbf6fc669ccf)

So this is a 64 bits binary which is dynamically linked and stripped

From the result of `checksec` we can see that:
- We have Full RELRO
- NX is enabled
- PIE is enabled

Ok next thing I did was to run it so as to get a general overview of what it does
![image](https://github.com/user-attachments/assets/f734009c-18c2-4e8c-b007-7d2c151de02c)

We see it prints out some banner thingy, receives our name and expects a secret code

With this I threw the binary into IDA and here's the main function
![image](https://github.com/user-attachments/assets/269c3186-64e2-47af-8f88-9cbe57d37c77)

```c
__int64 __fastcall main(int a1, char **a2, char **a3)
{
  __int64 v4; // [rsp+8h] [rbp-28h] BYREF
  char buf[10]; // [rsp+16h] [rbp-1Ah] BYREF
  unsigned int seed[3]; // [rsp+20h] [rbp-10h]
  int i; // [rsp+2Ch] [rbp-4h]

  *(_QWORD *)seed = time(0LL);
  sub_1209(0LL, a2);
  printf("\nEnter your name to access the system: ");
  fflush(stdout);
  read(0, buf, 0x50uLL);
  printf("\nWelcome Alien %s\nEnter the secret code to proceed: ", buf);
  fflush(stdout);
  __isoc99_scanf("%s", &v4);
  srand(seed[0]);
  if ( v4 == 0x69747563737975LL )
  {
    puts("\nCorrect Secret code..");
    puts("Welcome in the game space.\n");
    for ( i = 0; i <= 69; ++i )
    {
      if ( !(unsigned int)sub_126A() )
      {
        puts("Bye bye!");
        return 0LL;
      }
    }
    sub_150D();
  }
  else
  {
    puts("\nWrong Secret ..!");
  }
  return 0LL;
}
```

I won't explain in details what it does but the basic idea is this:
- Initializes a seed which is based on the current time
- Reads in at most 50 bytes of data into a buffer that can only hold up 10 bytes
- Reads in the secret code
- Calls srand with the seed so it's basically seeding with the current time
- Casts the secret code provided as a long and compares it against a hardcoded value: 0x69747563737975LL
- Based on if the code provided is right it would do another thing else it prints the error message

From this there are two obvious vulnerability:
- Buffer overflow via read()
- Buffer overflow via scanf()

I actually ignored it for now to know what would happen if we pass the comparism

So once we pass the check we get into this:

```c
   puts("\nCorrect Secret code..");
    puts("Welcome in the game space.\n");
    for ( i = 0; i <= 69; ++i )
    {
      if ( !(unsigned int)sub_126A() )
      {
        puts("Bye bye!");
        return 0LL;
      }
    }
    sub_150D();
  }
```

Basically it would loop 70 times and if after calling `sub_126A()` it doesn't return `1` it would print the error message then `returns`

Here's function `sub_126A` decompilation
![image](https://github.com/user-attachments/assets/9d22f744-5458-4b0a-8e05-acf933573e2e)

```c
__int64 sub_126A()
{
  _QWORD v1[21]; // [rsp+0h] [rbp-B0h]
  int v2; // [rsp+A8h] [rbp-8h] BYREF
  int v3; // [rsp+ACh] [rbp-4h]

  v1[0] = "1: Reach for the stars; you might just catch one!";
  v1[1] = "2: Ignite the cosmic flame within you!";
  v1[2] = "3: Celestial traveler, let's have some interstellar fun!";
  v1[3] = "4: Ready to embark on an astronomical journey?";
  v1[4] = "5: Buckle up, it's time for a cosmic adventure!";
  v1[5] = "6: You're about to enter a universe of possibilities.";
  v1[6] = "7: Get ready for an amazing celestial experience!";
  v1[7] = "8: Welcome, let's launch this cosmic party!";
  v1[8] = "9: Exciting times await in the vast cosmos, welcome aboard!";
  v1[9] = "10: Your journey through the galaxies begins now!";
  v1[10] = "11: Step into the cosmos of possibilities.";
  v1[11] = "12: Join the cosmic fun and enjoy the interstellar ride!";
  v1[12] = "13: The journey to the stars begins with you!";
  v1[13] = "14: Prepare for a fantastic astral experience.";
  v1[14] = "15: Welcome to the universe of endless possibilities.";
  v1[15] = "16: The cosmic stage is yours, shine like a supernova!";
  v1[16] = "17: Time to shine bright like distant stars and have some fun!";
  v1[17] = "18: Embrace the astronomical adventure that lies ahead.";
  v1[18] = "19: You're in for a celestial treat!";
  v1[19] = "20: The cosmic fun starts now!";
  printf("\nGuess the next alien quote number.\nChoose a number from 1 to 20:");
  fflush(stdout);
  __isoc99_scanf("%d", &v2);
  if ( v2 > 0 && v2 <= 20 )
  {
    v3 = (rand() + 8) % 20 + 1;
    printf("\nQuote | %s\n", (const char *)v1[v3]);
    if ( v3 == v2 )
    {
      puts("\nYou win.");
      return 1LL;
    }
    else
    {
      puts("\nYou lost.");
      return 0LL;
    }
  }
  else
  {
    puts("Invalid value!");
    return 0LL;
  }
}
```

Basically we just need to guess the right choice, and that's computed using a value returned from calling `rand()`

Ok good 

















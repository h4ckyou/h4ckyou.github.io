<h3> Battle CTF 2024 </h3>

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


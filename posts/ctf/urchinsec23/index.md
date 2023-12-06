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

Decompiling it in Ghidra shows this


I played as `@rizz` 🙂

![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/aa3e5b95-6373-493f-9ce9-c69069021017)

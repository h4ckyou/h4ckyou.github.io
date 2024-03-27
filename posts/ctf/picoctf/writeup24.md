<h3> PICOCTF '24 </h3>

#### Description: This was a fun ctf that took place from March 12 to March 26, 2024. I played with team *Fuji_*
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/b697be8a-2adb-48f3-8260-1db8ddfd8e69)
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/87b20483-b9c6-4cde-97b1-8abc8ee6cc32)


**I'll be giving writeup to challenges I solved**

<h3> Challenge Solved </h3>

## General Skills
- Super SSH
- Commitment Issues
- Time Machine
- Blame Game
- Collaborative Development
- Binhexa
- Binary Search
- Endianness
- Dont-you-love-banners
- SansAlpha

## Forensics
- Scan Surprise
- Verify
- CanYouSee
- Secret of the Polyglot
- Mob psycho
- Endianness-v2
- Blast from the past
- Dear Diary

## Reverse Engineering
- Packer
- FactCheck
- Classic Crackme 0x100
- WeirdSnake
- WinAntiDbg0x100
- WinAntiDbg0x200
- WinAntiDbg0x300

## Cryptography
- Interencdec
- Custom encryption
- C3
- Rsa Oracle

## Binary Exploitation
- Format String 0
- Heap 0
- Format String 1
- Heap 1
- Heap 2
- Heap 3
- Format  String 2
- Format String 3
- Babygame 03

### General Skills 10/10 :~

#### Super SSH
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/6baf5964-a045-4fd8-9e09-b75809b7cf4f)


We are to ssh as `ctf-player` to `titan.picoctf.net` at port `50832` with password `84b12bae`

So I just did that and got the flag :)
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/1ac9aae8-c943-4332-a423-d36682b8cffc)

```
Flag: picoCTF{s3cur3_c0nn3ct10n_07a987ac}
```

#### Commitment Issues
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/15c45383-53ca-49c9-ab78-515cf046c0f0)

We are given a zip file and after unzipping it showed a git directory in the `./drop-in` directory
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/6b7213b9-3563-4f2f-a95d-8d2494f69969)

Going over there shows this
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/daa04493-61f4-4cfb-a987-cb4be2c8220d)

From the challenge description we know the message was already deleted 

So I checked the git logs
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/079a61dd-5fc9-4c26-a3ea-df65d1984750)

The commit `87b85d7dfb839b077678611280fa023d76e017b8` was responsible in the creation of the flag

I checked it and got the flag
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/2fd81a96-e134-4e7b-9da6-da9c634e1af5)

```
Flag: picoCTF{s@n1t1z3_ea83ff2a}
```

#### Time Machine
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/18cb8d91-570c-47ca-bcad-029791f60309)

We are given a zip file and after unzipping it showed a git directory in the `./drop-in` directory (same as the previous challenge)
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/34c90ea7-fc66-40ae-a05b-6644d6f5370b)

Going over there shows this















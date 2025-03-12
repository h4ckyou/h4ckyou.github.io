<h3> Fetch The Flag CTF </h3>

![image](https://github.com/user-attachments/assets/0e0fd28f-0748-4ce2-b415-f7b68321237f)

This is my writeup for some of the challenges i solved

I did solve all reverse engineering but i was really busy with school so hence my writeup coming late

### Challenge Solved (not based on difficulty)
- Crab Shell
- Letter To Nums
- Math For Me
- PShell
- It's Go Time


#### Crab Shell
Checking file type
![image](https://github.com/user-attachments/assets/0de1fe75-3fef-4e22-b5fd-ac0e4b3636ae)

Running strings we get this
![image](https://github.com/user-attachments/assets/f0f01a67-9069-41ad-bf93-45aaff58376c)

This is a rust compiled program, we can also confirm by grepping it
![image](https://github.com/user-attachments/assets/f7c1de05-7134-4cd7-a154-a81f64bca683)

Running it we get this
![image](https://github.com/user-attachments/assets/6b828840-480a-408e-953b-68ff32dc2423)

It asks for a 16 byte key and it does validate the input length

Loading it up in IDA here's the main function
![image](https://github.com/user-attachments/assets/8e4ce70e-9222-4692-95f6-c15a60a7c57a)

I'm not so much familiar with rust reversing cause i don't know rust but i've looked at one or two decompilation before so i'm certain that the main program logic at `crabshell::main`

Decompiling it we have this
![image](https://github.com/user-attachments/assets/f3d9428e-7655-4535-b12d-ae24cbf19b6f)
![image](https://github.com/user-attachments/assets/cca302e1-cf63-4f6c-a1de-873b991204f7)

Looks so cryptic lmao!

Reading through it step by step it's clear that it will first print some text then receive our input
![image](https://github.com/user-attachments/assets/0836803a-b3a3-42a3-ab8f-9c466c044523)

Next it will make sure the received input length is 16 then it compares the input with some hardcoded value, if all the bytes matches it will then compute the md5 hash and print it out
![image](https://github.com/user-attachments/assets/0e913ed9-bad1-455a-be70-8bd8bfbce3c7)

So the important part is here:

```c
  {
    if ( *(_BYTE *)v1 == 49
      && *(_QWORD *)(v1 + 1) == 0x1F221731232D1F26LL
      && *(_DWORD *)(v1 + 9) == 1684542258
      && *(_BYTE *)(v1 + 13) == 100
      && *(_BYTE *)(v1 + 14) == 104
      && *(_BYTE *)(v1 + 15) == 104 )
    {
```

We simply just need to make sure the bytes it checks matches

Since IDA is so awesome it already defined the right data type making life easier for us

So `v1` is the buffer where it stores our input

Just a quick note:
- BYTE -> 1 byte
- WORD -> 2 bytes
- DWORD -> 4 bytes
- QWORD -> 8 bytes

With this we know that:

```
- v1[0] = 49
- v1[1:9] = 0x1F221731232D1F26
- v1[9:13] = 1684542258
- v1[13] = 100
- v1[14] = 104
- v1[15] = 104
```

We can just throw that in python and print it's byte representation

```python
import struct

v1 = [0] * 16

qword = 0x1F221731232D1F26
dword = 0x64681332

value1 = struct.pack("<Q", qword)
value2 = struct.pack("<I", dword)

v1[0] = 49
v1[1:9] = value1
v1[9:13] = value2
v1[13] = 100
v1[14] = 104
v1[15] = 104

expected = bytes(v1)

print(expected, len(expected))

with open("a.out", "wb") as f:
    f.write(expected)
```

Running it works and we get the flag
![image](https://github.com/user-attachments/assets/2a55049f-ce47-4464-a03c-47e23353c877)

```
Flag: flag{cc811d4486decc3379dd13688a46603f}
```




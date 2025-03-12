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

We can just throw that in python and print it's bytes representation

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

#### Letters To Num

We are given two files
![image](https://github.com/user-attachments/assets/9020ea56-fbde-499c-9b58-15d25619c2bb)

We can make assumption that the `letter2nums.elf` file encoded the original flag and `encflag.txt` is the result

Loading it up in IDA here's the main function
![image](https://github.com/user-attachments/assets/35a5c8bc-8634-48bc-9c10-6dbfc6e7174b)

First it calls the `readFlag` function passing a filename and an output buffer as the parameter
![image](https://github.com/user-attachments/assets/baf44057-f2df-46e1-b083-f1174b04354d)

The function simply reads the `flag.txt` file and stores the content in `flag_buf`

Next it calls the `c` function passing some text as first parameter, the `flag_buf` as the second parameter and an output buffer `buf` as the third parameter
![image](https://github.com/user-attachments/assets/1a8a714f-6ae1-47cc-81b4-cf2af2435daa)

What this simply does is to serializes the first message along with the plaintext flag into an output buffer

Then finally it calls the `writeFlag` function which takes an output filename and the buffer containing what we want to encode
![image](https://github.com/user-attachments/assets/1a8756f7-775a-4662-b9b3-02b4daf7ef03)

The function first opens the filename with flag set as `writable` then it gets the length of the `buf` by calling function `sl`
![image](https://github.com/user-attachments/assets/5346b467-a223-409a-9d9b-3f812cccc0c0)

The `sl` function calculates the length of the `buf` recursively 

Then finally it iterates through the size of the `buf` in chunks of 2 and calls the `encodeChars` function on `buf[i] and buf[i+1]` where the output is then stored in the file stream opened earlier
![image](https://github.com/user-attachments/assets/f9eb3a52-ff66-4918-a622-3054ae86a3b8)

The `encodeChars` function really doesn't do much

```c
__int64 __fastcall encodeChars(char byte1, char byte2)
{
  int result; // eax

  result = byte1 << 8;                          // upper byte
  LOWORD(result) = byte2;
  return (byte1 << 8) | (unsigned int)result;
}
```

It takes two bytes (byte1 and byte2) and packs them into a 16-bit integer

We can easily recover the plaintext

Here's my solve

```python
array = []

with open("encflag.txt", "r") as f:
    for line in f.readlines():
        value = line.strip()
        array.append(int(value))

decoded = b""

for i in range(len(array)):
    value = array[i].to_bytes(2, byteorder="big")
    decoded += value

print(decoded)
```

Running it we get the flag
![image](https://github.com/user-attachments/assets/e3ebd9b1-f0a9-42e8-b4b5-af86feb38fd1)

```
Flag: flag{3b050f5a716e51c89e9323baf3a7b73b}
```

#### Math For Me

We are given just a single executable
![image](https://github.com/user-attachments/assets/189cf6ff-35b5-415e-b522-971e430ad0c6)

If we run it we're asked to input a specific number
![image](https://github.com/user-attachments/assets/d97b1f1c-ee7b-44ec-89c5-1c53add7166c)

Loading it up in IDA here's the main function
![image](https://github.com/user-attachments/assets/952415c1-8390-4f4a-bbcb-155ea7ce45f0)

Basically based on the number provided it will validate if it's right then uses that number to generate the flag

That means the main thing is `check_number`
![image](https://github.com/user-attachments/assets/abe3cdde-b6ef-4954-8cf3-3a6656feead8)

Just a very basic math

```
(5 * a1 + 4) / 2 == 52
```

We just need to solve for `a1` in the equation

```
(5 * a1 + 4) = (52 * 2)
5 * a1 = (52 * 2) - 4
a1 = ((52 * 2) - 4) // 5
a1 = 20
```

This means the special number is 20
![image](https://github.com/user-attachments/assets/297e7245-641b-434f-b643-c0b155672ec1)

```
Flag: flag{h556cdd`=ag.c53664:45569368391gc}
```


























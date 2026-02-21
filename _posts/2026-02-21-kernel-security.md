---
title: Kernel Security
date: 2026-02-21 10:00:00 +0000
categories: [CTF, Writeup]
tags: [pwnable, pwncollege]
math: true
mermaid: true
media_subpath: /assets/posts/2026-02-21-Kernel-Security
image:
  path: completed.png
---

## Kernel Security

### Overview

Having completed the Kernel Security module at [pwn.college](https://pwn.college/system-security/), I decided to document my approach to the Level 10 challenge.

Interestingly, I solved it using a method different from the one originally intended

![completed](completed.png)

### Setup

Since I planned to debug locally, I needed to install the necessary tooling to replicate the challenge environment.

Fortunately, pwn.college provides a ready-to-use script that builds a kernel matching the exact version used in the dojo instance. This makes local debugging significantly easier.

You can find the repository here: [https://github.com/pwncollege/pwnkernel/tree/main](https://github.com/pwncollege/pwnkernel/tree/main)

Here's the compiled kernel boot image

```bash
mark@rwx:~/Desktop/Labs/PwnCollege/Kernel/pwnkernel$ file vmlinux bzImage 
vmlinux: ELF 64-bit LSB executable, x86-64, version 1 (SYSV), statically linked, BuildID[sha1]=eae7b711fb29722f5df763b3704c582490813ebf, with debug_info, not stripped
bzImage: Linux kernel x86 boot executable bzImage, version 5.4.0 (root@buildkitsandbox) #1 SMP Mon Oct 27 19:12:19 UTC 2025, RO-rootFS, swap_dev 0XA, Normal VGA
mark@rwx:~/Desktop/Labs/PwnCollege/Kernel/pwnkernel$
```

We can also extract the challenge's kernel module from the dojo

![challenge](challenge.png)
![scp](scp.png)

I then placed the kernel module into the uncompressed filesystem because on boot all kernel modules placed at `/` are loaded

A modification I also did was to disable switching to the user `ctf` for debug purpose (by commenting - see last line of the code)

```bash
mark@rwx:~/Desktop/Labs/PwnCollege/Kernel/pwnkernel$ cp babykernel_level10.1.ko fs/
mark@rwx:~/Desktop/Labs/PwnCollege/Kernel/pwnkernel$ cat fs/init 
#!/bin/sh

mount -t proc none /proc
mount -t sysfs none /sys
mount -t 9p -o trans=virtio,version=9p2000.L,nosuid hostshare /home/ctf
for f in $(ls *.ko); do
    insmod $f
done
sysctl -w kernel.perf_event_paranoid=1

cat <<EOF

Boot took $(cut -d' ' -f1 /proc/uptime) seconds

Welcome to pwn.college

EOF
chmod 600 /flag
chown 0.0 /flag
/bin/sh

#exec su -l ctf
mark@rwx:~/Desktop/Labs/PwnCollege/Kernel/pwnkernel$
```





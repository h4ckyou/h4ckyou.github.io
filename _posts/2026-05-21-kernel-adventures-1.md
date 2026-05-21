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
- **SMAP/SMEP/KPTI** isn't enabled.

The kernel version compiled is *4.19.81*:

```bash
mark@rwx:~/Desktop/Labs/HTB/Challenges/KernelAdventure1/release$ file bzImage 
bzImage: Linux kernel x86 boot executable bzImage, version 4.19.81 (sampriti@sampriti-xps) #1 SMP Fri Nov 29 14:56:26 EST 2019, RO-rootFS, swap_dev 0X7, Normal VGA
mark@rwx:~/Desktop/Labs/HTB/Challenges/KernelAdventure1/release$ 
```

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

I modified the *run.sh* script so that the *rootfs* directory is automatically compressed each time the VM boots.

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

Recall that *notes.txt* mentioned the password hashes had been zeroed out. We can confirm by checking it out.

```bash
mark@rwx:~/Desktop/Labs/HTB/Challenges/KernelAdventure1/release$ cd rootfs/
mark@rwx:~/Desktop/Labs/HTB/Challenges/KernelAdventure1/release/rootfs$ cd etc/
mark@rwx:~/Desktop/Labs/HTB/Challenges/KernelAdventure1/release/rootfs/etc$ cat passwd 
root:x:0:0:root:/root:/bin/sh
user:x:1000:1000:user:/home/user:/bin/sh
admin:x:1001:1001:admin:/home/admin:/bin/sh
mark@rwx:~/Desktop/Labs/HTB/Challenges/KernelAdventure1/release/rootfs/etc$ cat shadow
root:*:::::::
user:*:::::::
admin:*:::::::
mark@rwx:~/Desktop/Labs/HTB/Challenges/KernelAdventure1/release/rootfs/etc$
```

So currently there are 3 users:
- *root*
- *user*
- *admin*

The */etc/shadow* file confirms that the password hashes were removed, matching the words from *notes.txt*.

Next, let's inspect the *init* script, which is the first user-space process executed during system boot.

```bash
mark@rwx:~/Desktop/Labs/HTB/Challenges/KernelAdventure1/release/rootfs$ cat init 
#!/bin/sh
/bin/mount -t devtmpfs devtmpfs /dev
chown root:tty /dev/console
chown root:tty /dev/ptmx
chown root:tty /dev/tty
mkdir -p /dev/pts
mount -vt devpts -o gid=4,mode=620 none /dev/pts

mount -t proc proc /proc
mount -t sysfs sysfs /sys

echo 0 > /proc/sys/kernel/kptr_restrict
echo 0 > /proc/sys/kernel/dmesg_restrict

insmod mysu.ko
chmod 666 /dev/mysu

setsid cttyhack setuidgid 1000 sh

umount /proc
umount /sys

poweroff -d 1 -n -f
mark@rwx:~/Desktop/Labs/HTB/Challenges/KernelAdventure1/release/rootfs$
```

The *init* script shows that a kernel module (mysu.ko) is loaded during boot, and afterward a shell is spawned as the user account (UID 1000).

Interestingly it disables `kptr_restrict` and `dmesg_restrict`, which typically restrict kernel pointer visibility and access to kernel logs.

Well that's all for the file system analysis, now we will reverse the kernel module because that's our target.

We begin by analyzing the kernel module:

```bash
mark@rwx:~/Desktop/Labs/HTB/Challenges/KernelAdventure1/release$ cp rootfs/mysu.ko .
mark@rwx:~/Desktop/Labs/HTB/Challenges/KernelAdventure1/release$ file mysu.ko
mysu.ko: ELF 64-bit LSB relocatable, x86-64, version 1 (SYSV), BuildID[sha1]=a843ca9280a408d502d5a9fda75b99a8e262d16c, not stripped
mark@rwx:~/Desktop/Labs/HTB/Challenges/KernelAdventure1/release$ modinfo mysu.ko
filename:       /home/mark/Desktop/Labs/HTB/Challenges/KernelAdventure1/release/mysu.ko
description:    My Custom Su
license:        GPL
depends:        
retpoline:      Y
name:           mysu
vermagic:       4.19.81 SMP mod_unload 
mark@rwx:~/Desktop/Labs/HTB/Challenges/KernelAdventure1/release$
```

Opening the module in *IDA*, here's the constructor function:

```c
__int64 mysu_init()
{
  unsigned int v0; // edx
  unsigned __int64 v1; // rax

  printk(&unk_378);
  majorNumber = _register_chrdev(0LL, 0LL, 256LL, "mysu", &fops);
  if ( majorNumber >= 0 )
  {
    printk(&unk_3C2);
    mysuClass = _class_create(&_this_module, "mysu", &_class_create);
    if ( (unsigned __int64)mysuClass <= 0xFFFFFFFFFFFFF000LL )
    {
      printk(&unk_410);
      v1 = device_create(mysuClass, 0LL, (unsigned int)(majorNumber << 20), 0LL, "mysu");
      v0 = 0;
      mysuDevice = v1;
      if ( v1 > 0xFFFFFFFFFFFFF000LL )
      {
        class_destroy(mysuClass, 0LL, 0LL);
        _unregister_chrdev((unsigned int)majorNumber, 0LL, 256LL, "mysu");
        printk(&unk_440);
        return (unsigned int)mysuDevice;
      }
    }
    else
    {
      _unregister_chrdev((unsigned int)majorNumber, 0LL, 256LL, "mysu");
      printk(&unk_3E0);
      return (unsigned int)mysuClass;
    }
  }
  else
  {
    printk(&unk_398);
    return (unsigned int)majorNumber;
  }
  return v0;
}
```

This module registers a *character device*, which is exposed to user space as `/dev/mysu`.

The cleanup routine is responsible for properly removing this device and unregistering all associated kernel structures when the module is unloaded:

```c
__int64 mysu_exit()
{
  __int64 v0; // rsi
  __int64 v1; // rdx

  v0 = (unsigned int)(majorNumber << 20);
  device_destroy(mysuClass, v0);
  class_unregister(mysuClass);
  class_destroy(mysuClass, v0, v1);
  _unregister_chrdev((unsigned int)majorNumber, 0LL, 256LL, "mysu");
  return printk(&unk_465);
}
```

The module registers its file operations structure during initialization:

```c
majorNumber = _register_chrdev(0LL, 0LL, 256LL, "mysu", &fops);
```

The relevant entries in the `fops` structure are:

```c
.data:0000000000000570                 dq offset dev_read
.data:0000000000000578                 dq offset dev_write
```

This means the device supports only two main operations:

- **read()** -`dev_read`
- **write()** - `dev_write`

The *dev_read* function is invoked when a user-space process calls the read syscall on `/dev/mysu`.

```c
size_t __fastcall dev_read(__int64 filp, void *buf, unsigned __int64 size, __int64 offset)
{
  unsigned __int64 n; // [rsp+8h] [rbp-18h]

  n = size;
  if ( size > 0x20 )
    n = 0x20LL;
  memcpy(buf, &users, n);
  return n;
}
```

It ensures that the provided size is less than or equal to `0x20` before it copies the data stored at `users` to the user-space buffer.


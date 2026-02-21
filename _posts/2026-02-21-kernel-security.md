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

Since I planned to debug locally, I needed to have the necessary tooling and kernel build to replicate the challenge environment.

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

We also need to know how the kernel is booted in order to identify what protections are enabled

Here's the function that handles boot when we execute the `vm start` command on the dojo shell

```python
def extra_boot_flags():
    nokaslr = True
    if os.path.exists("/challenge/.kaslr"):
        nokaslr = False
    if args.nokaslr is not None:
        nokaslr = args.nokaslr

    nopti = False
    if os.path.exists("/challenge/.nopti"):
        nopti = True

    panic_on_oops = False
    if os.path.exists("/challenge/.panic_on_oops"):
        panic_on_oops = True

    result = []
    if nokaslr:
        result.append("nokaslr")

    if nopti:
        result.append("nopti")

    if panic_on_oops:
        result.append("oops=panic")
        result.append("panic_on_warn=1")

    return result

def start():
    bzImage = "/challenge/bzImage" if os.path.exists("/challenge/bzImage") else "/opt/linux/bzImage"
    kvm = os.path.exists("/dev/kvm")
    cpu = "host" if kvm else "qemu64"
    append = " ".join([
        "rw",
        "rootfstype=9p",
        "rootflags=trans=virtio",
        "console=ttyS0",
        "init=/opt/pwn.college/vm/init",
        *extra_boot_flags(),
        f"PATH={os.environ['PATH']}",  # PATH is safe (exec-suid)
    ])

    qemu_argv = [
        "/usr/bin/qemu-system-x86_64",
        "-kernel", bzImage,
        "-cpu", f"{cpu},smep,smap",
        "-fsdev", "local,id=rootfs,path=/,security_model=passthrough",
        "-device", "virtio-9p-pci,fsdev=rootfs,mount_tag=/dev/root",
        "-fsdev", "local,id=homefs,path=/home/hacker,security_model=passthrough",
        "-device", "virtio-9p-pci,fsdev=homefs,mount_tag=/home/hacker",
        "-device", "e1000,netdev=net0",
        "-netdev", "user,id=net0,hostfwd=tcp::22-:22",
        "-m", "2G",
        "-smp", "2" if kvm else "1",
        "-nographic",
        "-monitor", "none",
        "-append", append,
    ]

    if kvm:
        qemu_argv.append("-enable-kvm")

    if is_privileged():
        qemu_argv.append("-s")

    argv = [
        "/usr/sbin/start-stop-daemon",
        "--start",
        "--pidfile", "/run/vm/vm.pid",
        "--make-pidfile",
        "--background",
        "--no-close",
        "--quiet",
        "--oknodo",
        "--startas", qemu_argv[0],
        "--",
        *qemu_argv[1:]
    ]

    subprocess.run(argv,
                   stdin=subprocess.DEVNULL,
                   stdout=open("/run/vm/vm.log", "a"),
                   stderr=subprocess.STDOUT,
                   check=True)

```

I spawned a privileged instance so as to modify the code and add a `print` statement to see the full command!

![boot](boot.png)

With this I got the full startup command

```bash
/usr/bin/qemu-system-x86_64 \
    -kernel bzImage \
    -initrd $PWD/initramfs.cpio.gz \
    -cpu host,smep,smap \
    -enable-kvm \
    -fsdev local,security_model=passthrough,id=fsdev0,path=$HOME \
    -device virtio-9p-pci,id=fs0,fsdev=fsdev0,mount_tag=hostshare \
    -m 2G \
    -smp 2 \
    -nographic \
    -monitor none \
    -s \
    -append "console=ttyS0"
```

I just added that to the `launch.sh` file

![launch](launch.png)

### Analysis

From the setup code we can see that there are 3 protections enabled

(K)ASLR - Short for (Kernel) Address Space Layout Randomization that introduces another random element to make exploitation more difficult. Libraries and application-specific segments (like the stack, or heap) are loaded into different, random addresses upon each execution. This denies an attacker easy access to target addresses, functions, ROP gadgets and more. Exploitation typically requires an information leak of any kind.

SMEP - Supervisor Mode Execution Prevention, a kernel feature that marks all userland memory pages in the page table as non-executable, when a process's execution is in kernel-mode. This effectively eliminates the option to jump back to an attacker written and controlled user-land function (e.g. within the actual exploit). We require kernel ROP for effective exploitation. Common bypasses include pure in-kernel ROP chains, a stack pivot + user-land ROP, or abusing mmap'ed pages.

SMAP - Supervisor Mode Access Prevention, a complimentary feature to SMEP that also marks the same pages as non-accessible when execution happens in kernel-mode. As a result, user land page tables are not readable or writable anymore. S

To ease debugging, I disabled `kaslr` 

```bash
- -append "console=ttyS0"
+ -append "console=ttyS0 nokaslr"
```

Here's the module's info

![modinfo](modinfo.png)

Running the `launch.sh`, we can confirm that it's loaded

```
/ # lsmod
challenge 16384 0 - Live 0xffffffffc0000000 (O)
/ # ls -l
total 272
-rwxr-xr-x    1 ctf      1000        268536 Feb 21 10:14 babykernel_level10.1.ko
drwxr-xr-x    2 root     0             1900 Feb  7 16:08 bin
drwxr-xr-x    2 root     0               60 Oct 27 19:12 dev
drwxrwxr-x    2 ctf      1000            60 Feb  7 13:56 etc
-rw-------    1 root     0               19 Feb  7 13:56 flag
drwxr-xr-x    3 root     0               60 Feb  7 16:08 home
-rwxrwxr-x    1 ctf      1000           363 Feb  8 16:40 init
lrwxrwxrwx    1 root     0               11 Feb  7 16:08 linuxrc -> bin/busybox
dr-xr-xr-x   62 root     0                0 Feb 21 10:42 proc
drwxr-xr-x    2 root     0               40 Feb  7 16:08 root
drwxr-xr-x    2 root     0             1480 Feb  7 16:08 sbin
dr-xr-xr-x   12 root     0                0 Feb 21 10:42 sys
drwxr-xr-x    4 root     0               80 Feb  7 16:08 usr
/ # poweroff -f
[  133.984898] ACPI: Preparing to enter system sleep state S5
[  133.985627] reboot: Power down
mark@rwx:~/Desktop/Labs/PwnCollege/Kernel/pwnkernel$
```

Time to reverse engineer the kernel module!

This is the `init_module`

```c
int __cdecl init_module()
{
  proc_entry = (proc_dir_entry *)proc_create("pwncollege", 438LL, 0LL, &fops);
  printk(&unk_C20);
  printk(&unk_BD0);
  printk(&unk_C20);
  return 0;
}
```

This function registers a new entry in the proc filesystem and associates it with custom kernel handlers. Any interaction with `/proc/pwncollege` from user space will invoke the corresponding callbacks defined in the `file_operations` structure (`fops`).


```c
void __cdecl cleanup_module()
{
  if ( proc_entry )
    proc_remove();
}
```

This function simply deletes the registered entry.

Looking at the registered handlers, I saw just two

![ida_fops](ida_fops.png)

The `device_release` handler doesn't do much.

```c
__int64 device_release()
{
  return 0LL;
}
```

This means our target is at `device_write`

```c
ssize_t __fastcall device_write(file *file, const char *buffer, size_t length, loff_t *offset)
{
  ssize_t v4; // r12
  logger_t logger; // [rsp+0h] [rbp+0h] BYREF
  unsigned __int64 vars108; // [rsp+108h] [rbp+108h]

  vars108 = __readgsqword(0x28u);
  memset(&logger, 0, sizeof(logger));
  logger.log_function = (int (*)(const char *, ...))&printk;
  if ( length > 0x108 )
  {
    _warn_printk("Buffer overflow detected (%d < %lu)!\n", 264LL);
    BUG();
  }
  v4 = length - copy_from_user(&logger, buffer, length);
  logger.log_function((const char *)&logger);
  return v4;
}
```

This code isn't really much..

Here's the defined structure for `logger_t`

```c
00000000 struct logger_t // sizeof=0x108
00000000 {                                       // XREF: device_write/r
00000000     char buffer[256];
00000100     int (*log_function)(const char *, ...); // XREF: device_write+2E/w
00000100                                         // device_write:loc_5E/r
00000108 };
```

In short, this function handles writing to `/proc/pwncollege`, it ensures that the length doesn't exceed `0x108` then finally it copies the userspace buffer into the logger structure and executes the function pointer passing the address of the logger variable as the first parameter.

### Exploitation

From our analysis, the kernel module appears to not do much...however, it contains a critical vulnerability.

There is an 8-byte overflow, as the handler allows writing up to 0x108 bytes.

This overflow enables us to overwrite an adjacent function pointer, giving us control over the function that will be executed.

Despite being a single primitive, this bug is sufficient to achieve Local Privilege Escalation (LPE).

One obstacle, however, is that KASLR (Kernel Address Space Layout Randomization) is enabled, meaning kernel addresses are randomized at boot. As a result, we cannot reliably jump to hardcoded kernel addresses.

That said, if we are able to obtain a kernel address leak, we can defeat KASLR by calculating the kernel base address. Once the base is known, we can leverage any useful gadget within the kernel's .text section to construct our exploit.

#### Leaks

To obtain a kernel leak, I identified two possible approaches:
- Missing null termination, causing `printk` to read beyond the intended buffer and leak an adjacent kernel pointer.
- A format string vulnerability, which could be abused to disclose arbitrary kernel memory.

Both approaches rely on retrieving output from the kernel log ring buffer (`dmesg` / `vm logs`). Since `printk` writes directly to the kernel log, any unintended memory disclosure becomes observable from user space provided we have the permission.

In my solution, I chose to exploit the first method. The lack of proper null termination allows `printk` to continue reading into adjacent memory, ultimately leaking a kernel address. This leak is sufficient to recover the randomized kernel base and bypass KASLR.

After the `buf` is the address of the `printk` function so this means we will end up leaking `printk` address.

I'll show how it looks in memory, this is the code I wrote for filling up `buf` with `A's`

```c
#define _GNU_SOURCE
#include <unistd.h>
#include <fcntl.h>
#include <sys/ioctl.h>
#include <stdio.h>
#include <stdint.h>
#include <stdlib.h>
#include <string.h>
#include "log.h"

int main() {

    int fd = open("/proc/pwncollege", O_RDWR);
    
    if (fd <= 0) {
        logErr("Failed to open /proc/pwncollege");
        exit(1);
    }

    char payload[0x100] = {0};
    memset(payload, 'A', sizeof(payload)); 
    write(fd, payload, sizeof(payload));
    
    return 0;
}
```

Then compile and transfer it to the filesystem

```bash
mark@rwx:~/Desktop/Labs/PwnCollege/Kernel/pwnkernel$ musl-gcc leak.c -o leak -static
mark@rwx:~/Desktop/Labs/PwnCollege/Kernel/pwnkernel$ cp leak fs/
mark@rwx:~/Desktop/Labs/PwnCollege/Kernel/pwnkernel$
```

We can then boot the kernel.

Since the `-s` argument was specified in the `qemu` command this would enable remote debugging

![ss](ss.png)

Now we attach to the kernel using `gdb`

![one](gdb_one.png)
![two](gdb_two.png)
![three](gdb_three.png)

From this we just need to set a breakpoint at the point where the module is about to call the function pointer

To calculate the address we take the `mod_base + offset`

![modbase](base.png)
![disasm](disasm.png)

```bash
gef> b *device_write+89
Breakpoint 1 at 0xffffffffc0000069: file /tmp/tmpb5xkbd1s/challenge.c, line 78.
gef> 
```

Continuing execution and running `./leak` we hit the `breakpoint`

![leak1](leak1.png)
![leak2](leak2.png)

```bash
gef> telescope $rdi
```

From examining the memory layout, we observe that immediately after the buffer lies a pointer to `printk`.

Because the buffer is not properly null-terminated, `printk` continues reading past the intended boundary when logging the user-controlled input. As a result, it reads into the adjacent memory region which includes the stored function pointer.

![dmesg](dmesg.png)

With kernel address leak obtained we can defeat `KASLR`

![calculate](calculate.png)

#### LPE

With `KASLR` defeated this means we have just one arbitrary call as we control the address of `logger->log_function`

The intended solution was to make use of the `run_cmd` kernel function.

![run_cmd](run_cmd.png)

This function basically executes a command in userspace as root!

But to be honest, when I tried solving the challenge I couldn't make use of it and I eventually figured why - `/bin/sh` is interactive hence it wouldn't work (spawn a shell), alternatives like `chmod` to make the `flag` world-readable is sufficient.

So what now? 

Looking at the registers at the `call` instruction I saw this

![state](state.png)

We actually control `$rdi, [$rax], [$rbp]`, so i thought why not find possible gadgets that let's me stack pivot?

Hence my search started
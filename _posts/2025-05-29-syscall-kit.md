---
title: Syscall Kit 
date: 2026-05-29 03:00:00 +0000
categories: [CTF, Upsolve]
tags: [pwnable]
math: true
mermaid: true
media_subpath: /assets/posts/2026-05-29-syscall-kit
image:
  path: preview.png
---

## zer0pts 2020 - Syscall Kit

### Overview

*Syscall Kit* is a hard rated pwnable challenge created by `ptr-yudai`.

It is simply an emulator written in C++ that's used to execute user-provided system calls.

There are some restrictions however, and our goal is to pop shell from this somewhat restricted sandbox.

You can download the challenge attachments [here](https://github.com/zer0pts/zer0pts-CTF-2020/tree/master/syscall%20kit/distfiles)

### Analysis

The challenge just contains two files:
- **chall**
- **main.cpp**

Here are the protections enabled on the binary.

```bash
mark@rwx:~/Desktop/Practice/BinExp/Challs/STACK/SyscallKit$ checksec chall
[*] '/home/mark/Desktop/Practice/BinExp/Challs/STACK/SyscallKit/chall'
    Arch:       amd64-64-little
    RELRO:      Full RELRO
    Stack:      Canary found
    NX:         NX enabled
    PIE:        PIE enabled
    Stripped:   No
mark@rwx:~/Desktop/Practice/BinExp/Challs/STACK/SyscallKit$ 
```

When we run the program, we are asked to give it a syscall and it's argument.

![one](one.png)

In this case, I used the `exit` syscall whose `sys_num == 60`, and from the return value we can see it infact does what it says.

Since we are given the source code, we don't have to reverse engineer the binary.

Here's the source:

```cpp
/**
 * syscall kit - WinterKosenCTF 2020
 *
 * This application is (maybe) made for educational purpose
 * and for those who learn system calls.
 */
#include <iostream>
#include <sys/syscall.h>

class Emulator {
private:
  unsigned long rax;
  unsigned long rdi;
  unsigned long rsi;
  unsigned long rdx;
  virtual void set(std::string, unsigned long&);
  virtual int check();
  virtual void syscall();
public:
  Emulator();
  virtual void emulate();
};

/**
 * Constructor
 */
Emulator::Emulator() {
  this->rax = 0;
  this->rdi = 0;
  this->rsi = 0;
  this->rdx = 0;
}

/**
 * Read system call number and arguments
 */
void Emulator::set(std::string msg, unsigned long &reg) {
  std::cout << msg;
  std::cin >> reg;
  if (!std::cin.good()) exit(1);
}

/**
 * Filter dangerous system calls
 */
int Emulator::check() {
  if (this->rax >= 0x40000000)   return 1; // x32 ABI is dangerous!
  if (this->rax == SYS_open)     return 1; // never open files
  if (this->rax == SYS_openat)   return 1;
  if (this->rax == SYS_write)    return 1; // no more leak
  if (this->rax == SYS_read)     return 1; // no more overwrite
  if (this->rax == SYS_sendfile) return 1;
  if (this->rax == SYS_execve)   return 1; // of course not!
  if (this->rax == SYS_execveat) return 1;
  if (this->rax == SYS_ptrace)   return 1; // may ruine the program
  if (this->rax == SYS_fork)     return 1;
  if (this->rax == SYS_vfork)    return 1;
  if (this->rax == SYS_clone)    return 1;
  return 0;
}

/**
 * Call syscall
 */
void Emulator::syscall() {
  asm volatile ("movq %0, %%rdi":: "a"(this->rdi));
  asm volatile ("movq %0, %%rsi":: "a"(this->rsi));
  asm volatile ("movq %0, %%rdx":: "a"(this->rdx));
  asm volatile ("movq %0, %%rax":: "a"(this->rax));
  asm volatile ("syscall");
  asm volatile ("movq %%rax, %0": "=a"(this->rax));
}

/**
 * Run emulator
 */
void Emulator::emulate(void)
{
  int i;
  for(i = 0; i < 10; i++) {
    std::cout << "=========================" << std::endl;
    this->set("syscall: ", this->rax);
    this->set("arg1: ", this->rdi);
    this->set("arg2: ", this->rsi);
    this->set("arg3: ", this->rdx);
    
    std::cout << "=========================" << std::endl;
    
    if (this->check()) {
      std::cerr << "syscall=" << this->rax << " is not allowed" << std::endl;
      continue;
    } else {
      this->syscall();
      std::cout << "retval: " << std::hex << this->rax << std::endl;
    }
  }

  std::cout << "Bye!" << std::endl;
}

Emulator *m;

void setup(void)
{
  std::setbuf(stdin, NULL);
  std::setbuf(stdout, NULL);
  std::setbuf(stderr, NULL);

  m = new Emulator();
}

int main(void)
{
  setup();
  m->emulate();
  exit(0);
}
```

The code is small, but I’ll walk through each section.

First, there is a class named `Emulator`. It contains four private attributes representing the `x86_64` system call calling convention registers, along with four virtual methods and 1 public virtual method.

```cpp
class Emulator {
private:
  unsigned long rax;
  unsigned long rdi;
  unsigned long rsi;
  unsigned long rdx;
  virtual void set(std::string, unsigned long&);
  virtual int check();
  virtual void syscall();
public:
  Emulator();
  virtual void emulate();
};
```

This is the constructor. It simply initializes all of the object's register fields to zero:

```cpp
Emulator::Emulator() {
  this->rax = 0;
  this->rdi = 0;
  this->rsi = 0;
  this->rdx = 0;
}
```

The main function first initializes the object then calls the `emulate` method:

```cpp
void setup(void)
{
  std::setbuf(stdin, NULL);
  std::setbuf(stdout, NULL);
  std::setbuf(stderr, NULL);

  Emulator *m = new Emulator();
}

int main(void)
{
  setup();
  m->emulate();
  exit(0);
}
```

The `emulate` method runs for 10 iterations. On each iteration, it sets the object's register fields using `Emulator::set`.

After the registers are set, it then goes ahead to call `Emulator::check`, if the return value is `true` it would simply `continue` else it calls `Emulator::syscall`.

```cpp
void Emulator::emulate(void)
{
  int i;
  for(i = 0; i < 10; i++) {
    std::cout << "=========================" << std::endl;
    this->set("syscall: ", this->rax);
    this->set("arg1: ", this->rdi);
    this->set("arg2: ", this->rsi);
    this->set("arg3: ", this->rdx);
    
    std::cout << "=========================" << std::endl;
    
    if (this->check()) {
      std::cerr << "syscall=" << this->rax << " is not allowed" << std::endl;
      continue;
    } else {
      this->syscall();
      std::cout << "retval: " << std::hex << this->rax << std::endl;
    }
  }

  std::cout << "Bye!" << std::endl;
}

void Emulator::set(std::string msg, unsigned long &reg) {
  std::cout << msg;
  std::cin >> reg;
  if (!std::cin.good()) exit(1);
}
```

Our main point of interest is `Emulator::check`:

```cpp
int Emulator::check() {
  if (this->rax >= 0x40000000)   return 1; // x32 ABI is dangerous!
  if (this->rax == SYS_open)     return 1; // never open files
  if (this->rax == SYS_openat)   return 1;
  if (this->rax == SYS_write)    return 1; // no more leak
  if (this->rax == SYS_read)     return 1; // no more overwrite
  if (this->rax == SYS_sendfile) return 1;
  if (this->rax == SYS_execve)   return 1; // of course not!
  if (this->rax == SYS_execveat) return 1;
  if (this->rax == SYS_ptrace)   return 1; // may ruine the program
  if (this->rax == SYS_fork)     return 1;
  if (this->rax == SYS_vfork)    return 1;
  if (this->rax == SYS_clone)    return 1;
  return 0;
}
```

This method prevents the use of specific system calls, as well as any syscall value that falls into the x32 ABI range.

Conceptually, it behaves like a simple seccomp filter. If the syscall number in `rax` matches one of the blocked syscalls, `check()` returns `1`, meaning the syscall should be rejected. This is similar to a seccomp rule using `SCMP_ACT_KILL_PROCESS`, where attempting to execute a blocked syscall causes the process to be terminated.

As expected, `Emulator::syscall` uses inline assembly to load the CPU registers with the values stored in the object, then executes the `syscall` instruction.

After the syscall runs, its return value is placed in `rax`, and that value is then written back into the object's `rax` field.

The return value is also printed (as shown in the src code).

```cpp
void Emulator::syscall() {
  asm volatile ("movq %0, %%rdi":: "a"(this->rdi));
  asm volatile ("movq %0, %%rsi":: "a"(this->rsi));
  asm volatile ("movq %0, %%rdx":: "a"(this->rdx));
  asm volatile ("movq %0, %%rax":: "a"(this->rax));
  asm volatile ("syscall");
  asm volatile ("movq %%rax, %0": "=a"(this->rax));
}
```

### Exploitation

What's the vulnerability?

Well, there actually isn't any vulnerability

The challenge description says this:

```
It's a good tool to learn syscall, isn't it?
```

So we somehow need to leverage this emulator to trigger a syscall that would eventually spawn a shell.

Looking at the setup, we can only control 3 argument of the `syscall` of our choosing.

At the same time, it blocks so many syscalls that we could've easily used to gain a shell.

I'm going to be using this linux kernel syscall table as a [reference](https://syscalls.mebeim.net/?table=x86/64/x64/latest)

As of the latest kernel version (v6.17) there are **365 syscalls**.

Does it mean we need to go through all the syscalls (354) not blocked by the emulator?

Not necessarily...

The approach I took was to actually parse all the syscalls based on the number of argument it takes.

There's a json export of the syscall table [here](https://syscalls.mebeim.net/db/x86/64/x64/latest/table.json)

I wrote a script to parse all the syscalls I can use that makes use of only 3 or lesser arguments.

```python
import json

NUMBER = [0, 1, 2, 0x101, 0x28, 0x3b, 0x142, 0x65, 0x39, 0x3a, 0x38]
TABLE = "table.json"

with open(TABLE, "r") as f:
    dataset = json.load(f)

syscalls = dataset["syscalls"]
output = {
    "syscall": []
}

for syscall in syscalls:
    if (len(syscall["signature"]) <= 3) and (syscall["number"] not in NUMBER):
        output["syscall"].append(syscall)

# print(len(output["syscall"]))
print(json.dumps(output))
```

Although doing that only just reduces the potential syscall we can make use of to **236**.

It's still a lot.

![two](two.png)

I was thinking of spawning a local instance of the syscall table since it's [open source](https://github.com/mebeim/linux-syscalls) but that's just a lot of work and tbf as of *2020* it never existed.

Luckily the UI is awesome, it has a view where we can see the arguments needed.

![three](three.png)

My goal still remained the same, check out the syscalls that uses less or equal to 3 number of arguments.

Here are the syscalls I found interesting to check:

```c
int brk(void *addr);
int mprotect(unsigned long start, size_t len, unsigned long prot);
ssize_t readv(int fd, const struct iovec *iov, int iovcnt);
ssize_t writev(int fd, const struct iovec *iov, int iovcnt);
int syscall(SYS_arch_prctl, int op, unsigned long addr);
// ....
```

Firstly, we need to make our goal clear. Our goal is to gain `$rip` control.

What possible way can this be achieved?

One way would be a virtual function table (vtable) hijack.

C++ is an object oriented programming language.

Virtual functions is a key mechanism to support polymorphism in C++.

For each class with virtual functions, depending on the class inheritance hierarchy, the compiler will create one or more associated virtual function table (vtabe).

Looking at the object's initialization, we can see that the `Emulator` instance is allocated on the heap:

```cpp
void setup(void)
{
  std::setbuf(stdin, NULL);
  std::setbuf(stdout, NULL);
  std::setbuf(stderr, NULL);

  m = new Emulator();
}
```

Here's the heap layout after initialization:

![four](four.png)

```gdb
gef> emu_dump 0x5555556162b0
====== Emulator @ 0x5555556162b0 ======
[+] vtable            : 0x555555602ce0
[+] virtual functions
    [0] -> 0x555555401114
    [1] -> 0x55555540116e
    [2] -> 0x555555401290
    [3] -> 0x5555554012d8
===============================
```

Because the vtable pointer itself resides in a heap-allocated object, it becomes a writable target.

If we can forge the vtable, then any subsequent virtual method call on the object would dereference our fake vtable and jump to our controlled function pointer instead.










### Resources
- [https://www.slideshare.net/slideshow/pwning-in-c-basic/58370781](https://www.slideshare.net/slideshow/pwning-in-c-basic/58370781)
- [https://syscalls.mebeim.net/?table=x86/64/x64/latest](https://syscalls.mebeim.net/?table=x86/64/x64/latest)
- [https://elixir.bootlin.com/linux/v6.17/source/arch/x86/kernel/process_64.c#L867](https://elixir.bootlin.com/linux/v6.17/source/arch/x86/kernel/process_64.c#L867)
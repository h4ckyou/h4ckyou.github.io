---
title: Tiny Machine
date: 2025-12-06 22:00:00 +0000
categories: [CTF, Dreamhack]
tags: [pwnable]
math: true
mermaid: true
media_subpath: /assets/posts/2025-12-07-Tiny-Machine
image:
  path: dreamhack.png
---

## Dreamhack - Tiny Machine

### Overview

The **Tiny Machine** challenge implements a simple 8-bit register-based virtual machine written in Python. The VM loads the flag into memory, allocates space for our input right after it, and finally places the VM bytecode at the end meaning all data are laid out contiguously in memory.

The vulnerability comes from how the VM handles input, there's a buffer overflow during the read operation, allowing user-controlled bytes to overwrite adjacent memory, including parts of the VM program itself. Any invalid opcode or runtime exception causes the VM to exit. 

The VM intended functionality is to read our input and print it out back, but we will leverage the vulnerability to leak the flag directly from memory.

### Challenge Analysis

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

Looking through the code we see some handy comments for each switch cases in the **TinyMachine** class, and that gives us an idea of what each opcode does.

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
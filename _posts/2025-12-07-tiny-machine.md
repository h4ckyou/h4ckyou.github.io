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

Overview: The **Tiny Machine** challenge implements a simple 8-bit register-based virtual machine written in Python. The VM loads the flag into memory, allocates space for our input right after it, and finally places the VM bytecode at the end meaning all data are laid out contiguously in memory.

The vulnerability comes from how the VM handles input, there's a buffer overflow during the read operation, allowing user-controlled bytes to overwrite adjacent memory, including parts of the VM program itself. Any invalid opcode or runtime exception causes the VM to exit. 

The VM intended functionality is to read our input and print it out back, but we will leverage the vulnerability to leak the flag directly from memory.

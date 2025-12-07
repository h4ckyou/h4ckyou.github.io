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

Overview: The **Tiny Machine** challenge is a 8-bits register based virtual machine written in Python. The flag is loaded in to memory and the memory comprises of our *flag + user input + machine code* all adjacent in memory. There's a buffer overflow in the vm memory due to how the vm handles our input. Invalid instruction execution or any sort of exception are handled to make the program exit. The vm intended functionality is to read our input and print it out back, but we will leverage the vulnerability to leak the flag.


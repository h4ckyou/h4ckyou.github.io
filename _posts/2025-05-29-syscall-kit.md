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

## Zer0pts 2020 - Syscall Kit

### Overview

*Syscall Kit* is a hard rated pwnable challenge created by `ptr-yudai`.

It is simply an emulator written in C++ that's used to execute user-provided system calls.

There are some restrictions however, and our goal is to pop shell from this somewhat restricted sandbox.

You can download the attachment [here](https://github.com/zer0pts/zer0pts-CTF-2020/tree/master/syscall%20kit/distfiles)

### Analysis

The challenge just contains two files:
- **chall**
- **main.cpp**


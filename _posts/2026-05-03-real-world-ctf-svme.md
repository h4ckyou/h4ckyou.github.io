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

The challenge files can be found [here]()

The bug is an *out-of-bounds read/write* in the VM memory layout.

By abusing it, you can corrupt VM state and eventually get code execution.

### Analysis


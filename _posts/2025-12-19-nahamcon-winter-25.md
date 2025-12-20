---
title: NahamCon Winter CTF 2025
date: 2025-12-20 17:00:00 +0000
categories: [CTF, Writeup]
tags: [pwnable]
math: true
mermaid: true
media_subpath: /assets/posts/2025-12-19-Nahamcon-Winter
image:
  path: preview.png
---

## NahamCon Winter CTF 2025

### Overview

This writeup covers all pwn challenges from NahamCon Winter CTF 2025. The event featured two pwnable challenges: VulnBank and Snorex.

### VulnBank

#### Challenge Information
- **Difficulty**: Medium
- **First Blood**: true

VulnBank requires chaining multiple vulnerabilities to achieve code execution. The exploit path involves:

1. Exploiting a format string vulnerability to leak memory addresses and the authentication PIN
2. Using the leaked PIN to bypass authentication
3. Triggering a buffer overflow to redirect execution to the win function

#### Solution


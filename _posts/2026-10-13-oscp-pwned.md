---
title: OSCP Pwned
date: 2026-10-13 11:18:00 +0100
categories: [Blog]
tags: [OSCP, certification]
math: true
mermaid: true
media_subpath: /assets/posts/2026-10-13-oscp-pwned
image:
  path: pwned.png
---

## OSCP

### Overview

Well well, back in January I set myself a goal to get the OSCP and CPTS this year, and here I am now... with the OSCP cert.

![oscp badge](oscp-badge.png)
_OSCP+_

The OSCP (OffSec Certified Professional) is [OffSec](https://www.offsec.com/)'s pentesting cert that comes with the **PEN-200** course. The exam is fully hands-on: you get *23 hours 45 minutes* to hack into a set of machines, then another *24 hours* to write and submit your report.

The exam has:
- An **Active Directory** set of 3 machines (40 points)
- 3 **standalone** machines (20 points each, 10 for user and 10 for root)

You need *70* out of *100* points to pass.

### Study Process

I got my exam voucher on the 9th of September 2026, and my goal was to sit the exam before the 16th of October 2026 (hmmm 👀).

The course covers a lot of ground, including:
- Enumeration and information gathering (including vulnerability scanning)
- Web attacks like XSS, Command Injection, Directory Traversal, File Uploads and SQL Injection
- Client side attacks, password attacks and a bit of Anti-Virus evasion
- Windows and Linux privilege escalation
- Pivoting and tunneling
- Attacking Active Directory and moving laterally in it
- Enumerating and attacking AWS cloud infrastructure
- Tools like Nmap, Metasploit, Burp Suite, Hydra, Nessus, sqlmap and Shellter

I wasn't exactly new to most of this, so I speedran the course content in a week and moved straight to the challenge labs. I finished all of them in about 2 weeks.

![challenge labs](challenge-labs.png)
_PEN-200 Challenge Labs_

After that I bought an HTB subscription and solved all the machines on [TJ Null's OSCP list](https://docs.google.com/spreadsheets/u/1/d/1dwSMIAPIam0PuRBkCiDI88pU3yzrqqHkDtBngUHNCw8/htmlview).

My exam was scheduled for the 10th of October 2026 at 8 PM. That week I was busy with other stuff, so I didn't really grind much before it.

### Exam Day

I hopped on the call at 7:45 PM and waited for the exam to start. There were some issues, so I ended up starting around 8:30 PM.

I'd advise starting with the AD set because it's pretty straightforward (do OSCP A, B and C from the labs to get a feel for it). I documented as I went, and within 2 hours I had compromised the whole AD set.

That looked promising, so I went straight to the standalones. I got 2 Windows boxes and 1 Linux box.

I started with the Linux one because tbh I enjoy breaking into Linux more than Windows (but welp, lately I've been enjoying Windows too xD). I spent about 2 hours on it and couldn't get a foothold.

I almost started panicking, so I took a short break (a 5 minute walk to calm myself down) and then moved on to the Windows boxes.

I compromised both of them in 2 hours, and by 2 AM I had 80 points, which is enough to pass.

Since I was hell bent on solving that Linux box (and there was still plenty of time), I went back to hunting for the foothold. I worked on it for another hour, and at 3 AM I stopped to get some sleep.

I woke up around 6 AM with my brain fully refreshed and ready to pwn. I continued on the box and got the foothold by 8 AM 🎉

Privesc took me about 1 hour, and that was it, 100 points.

### Some Side Notes

Honestly, part of what pushed me to take the exam was that my teammate (Theory) recently passed his, so that pressure was definitely there.

I solved a lot of labs before the exam. Privesc can be tricky, but I think all that practice is what made it feel easy for me.

I didn't make many writeups while studying because duhh, writeups are hard to write.

### Conclusion

Doing the OSCP gave me the satisfaction of getting a "well known" cert, but I won't lie... in terms of difficulty, CPTS mogs it lol.

I'll keep working on my skills and getting better than I am now.

My next goal is the Blue Belt @ pwn.college (so my next blog post might be about that... or not?).

Thanks for reading, and to anyone preparing for the OSCP: enumerate, enumerate, enumerate!

That's all! ありがとうございます！😊

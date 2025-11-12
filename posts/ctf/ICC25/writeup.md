<h3> International Cybersecurity Challenge 2025 </h3>

Hey guys, h4cky0u here, I participated with team AFRICC at the ICC 2025 Tokyo, Japan.
<img width="1920" height="892" alt="image" src="https://github.com/user-attachments/assets/df0bbfd0-9b7d-425f-809c-92c7cfe66fcd" />

I mainly focused on the binary exploitation challenges where i solved 3/6 challenges.

This writeup contains the solution for the challenge named `Hoard` which had three solves and i was the 3rd blood..
<img width="1917" height="738" alt="image" src="https://github.com/user-attachments/assets/bd0cfbd8-defc-41f8-8dc2-034613841a10" />

```
Name: Hoard
Desc: Hoarding flags in a CTF is a shameful behavior and should be stopped.
Author: ptr-yudai
Link: http://hoard.org/
```

Here's the link to the attachment: [link](https://github.com/h4ckyou/h4ckyou.github.io/blob/main/posts/ctf/ICC25/files/firectf_icc-2025-whylz_distfiles_hoard-6543862fd682e5d69103645ac29369e3.tar)

We are provided with this files

```
~/Desktop/CTF/ICC25/Hoard/hoard ❯ ls -l
.rw-r--r-- mark mark 165 B  Thu Jan  1 00:00:00 1970 compose.yml
.rw-r--r-- mark mark 424 B  Thu Jan  1 00:00:00 1970 Dockerfile
.rw-r--r-- mark mark  11 B  Thu Jan  1 00:00:00 1970 flag.txt
.rwxr-xr-x mark mark  16 KB Thu Jan  1 00:00:00 1970 hoard
.rwxr-xr-x mark mark 473 KB Thu Jan  1 00:00:00 1970 libhoard.so
.rw-r--r-- mark mark 749 B  Thu Jan  1 00:00:00 1970 main.c
.rw-r--r-- mark mark  43 B  Thu Jan  1 00:00:00 1970 run
```

Kinda weird the timestamp all shows `Thu Jan 1 1970` when today's date is `Wed Nov 12 2025`

Looking through the docker file:

```
FROM ubuntu:24.04@sha256:04f510bf1f2528604dc2ff46b517dbdbb85c262d62eacc4aa4d3629783036096 AS base
RUN apt-get update && apt-get install libstdc++6
WORKDIR /app
ADD --chmod=555 run .
ADD --chmod=555 hoard .
ADD --chmod=555 libhoard.so .
ADD --chmod=444 flag.txt /flag.txt
RUN mv /flag.txt /flag-$(md5sum /flag.txt | awk '{print $1}').txt

FROM pwn.red/jail
COPY --from=base / /srv
ENV JAIL_TIME=300 JAIL_CPU=100 JAIL_MEM=10M
```

It basically just generates a random file name (this probably suggesting our goal is to get code execution) before setting up the red pwn jail.

So the important files we need to check now are: `run, hoard & libhoard.so`

The first file: basically sets the `LD_PRELOAD` variable to the shared library `libhoard.so`

```bash
#!/bin/sh
LD_PRELOAD=./libhoard.so ./hoard
```

We are given the binary source code so there's no need for reverse engineering...

```c
#include <stdlib.h>
#include <string.h>
#include <unistd.h>

void reads(const char *prompt, char *buf, size_t len) {
  write(1, prompt, strlen(prompt));
  for (size_t i = 0; i < len; i++) {
    if (read(0, buf + i, 1) != 1)
      _exit(1);
    if (buf[i] == '\n') {
      buf[i] = '\0';
      break;
    }
  }
}

unsigned readi(const char *prompt) {
  char buf[0x10] = { 0 };
  reads(prompt, buf, sizeof(buf)-1);
  return (unsigned)atoi(buf);
}

char *note;

int main() {
  for (size_t i = 0; i < 0x100; i++) {
    switch (readi("> ")) {
      case 1: reads("data: ", note = malloc(8), 8); break;
      case 2: write(1, note, strlen(note)); write(1, "\n", 1); break;
      case 3: free(note); break;
      default: _exit(0);
    }
  }
  _exit(0);
}
```

Pretty straight forward code
- We can make up to 256 allocations where the size is constant
- The pointer is stored in the global variable `note`
- We can free the pointer stored in note as many times as we want

Some things to take note of:
- No IO functions being used
- _exit() is used

So now that we know how the code works, how to exploit it? 

Well the bug there is pretty obvious, after it frees the chunk it doesn't set the pointer to null this means we can double free a chunk and as well a Read-After-Free.

From the challenge description and setup code we see that it makes use of the `libhoard.so` file

I wasn't familiar with what Hoard meant but luckily the link to the source was given
<img width="1920" height="697" alt="image" src="https://github.com/user-attachments/assets/5c1f6dd8-6ff8-4934-ae2b-891b428b979d" />

So `Hoard` is essentially a memory allocator, others we have are `dlmalloc, ptmalloc, jemalloc` etc.

The project is open source so we can grab the source code from: [here](https://github.com/emeryberger/Hoard)

Side Note: When I started solving this challenge I didn't see any reference to how it works in details exactly (maybe i didn't search well enough) so i kinda left it till i saw it got blooded and i went back to give it a try... 



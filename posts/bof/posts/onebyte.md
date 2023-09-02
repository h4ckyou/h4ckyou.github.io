<h3> DUCTF 2023: One Byte </h3>

![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/68d8d008-53af-4ba1-b5ca-64e8631ff0ff)

We are given the binary and it's source code

Here's the C source:
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/815e5671-519a-4466-85f4-11747e60342d)

```c
#include <stdio.h>
#include <unistd.h>
#include <stdlib.h>

void init() {
    setvbuf(stdout, 0, 2, 0);
    setvbuf(stdin, 0, 2, 0);
}

void win() {
    system("/bin/sh");
}

int main() {
    init();

    printf("Free junk: 0x%lx\n", init);
    printf("Your turn: ");

    char buf[0x10];
    read(0, buf, 0x11);
}
```

Looking at it we can see the program doesn't do much!

Here's what it does:
- Defines 3 functions i.e init, win, main
- The init function does some buffering
- The win function tends to spawn a sh shell
- The main function gives us a binary leak of the init function
- Then it receives our input and store in the buf array

The vulnerability lies in the read call because:
- The buffer is set to hold up only `0x10` bytes
- But we are reading in `0x11`

That gives us a one byte buffer overflow

At first I was like this is too easy and what the hell is the leak for 

Trust me it's easy but I spent about an hour solving it lol


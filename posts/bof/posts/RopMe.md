<h1> Learning....</h1>

I made this C file inorder to practice ROP by calling `mprotect()` thereby making the stack executable and popping shell 🐚

Source:

```c
#include <stdio.h>

void greet_me(){
    char name[0x64];
    
    puts("Prove your worth hackerman!");
    gets(name);

}

int main(int argc, char *argv[]){
    greet_me();

    return 0;
}
```

Compile using:
- gcc rop.c -no-pie -static


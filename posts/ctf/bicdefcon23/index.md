<h3> BIC DEFCON CTF 2023 </h3>

### Description: This was a fun ctf I did during the weekend and it taught me new things >3

<h3> Challenge Solved: </h3>

## Pwn
-  Puts in boot
-  Karma
-  Dubdubdub
-  Shellstorm
-  Breakup

### Puts in boot [First Blood 🩸]

We are given a binary file attached to it

Checking the file type shows this
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/89cb3511-2060-42f3-b332-c7ba455220ed)

We are working with a x64 binary which is dynamically linked and not stripped

From the result of checksec on this binary we can tell that the binary has no protection enabled on it

What looks interesting is the fact NX is disabled meaning that the stack is executable

And with that it's possible for us to place shellcode on the stack and execute it 

Anyways let us see what the binary does

Running it shows this
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/ad11f512-9eb4-4138-8d9e-8578b3be4b16)

It receives our option prints out some words and exits

To understand the vulnerability in this binary I'll read the decompiled code 

Using ghidra I decompiled the binary 

Here's the main function
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/36b3d5a5-589a-489c-8e92-0bc4b1cf6b2a)
```c

void main(void)

{
  do {
    AI();
  } while( true );
}
```

It calls the AI function while it returns true

Let us check the AI function
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/5ab50d20-a781-45d5-bc59-bcebb03a7926)
```c
void AI(void)

{
  char buffer [79];
  char option;
  
  puts("Know of Andrej Karpathy?");
  puts(
      "A: I\'m sorry, who?\nB: Why should I?\nC: Uum, lemme Google and come back\nD: Ofcourse I do!"
      );
  fflush(stdout);
  __isoc99_scanf("%1s",&option);
  if (option == 'A') {
    puts("Andrej Karpathy!! You know, famous computer scientist?");
    puts("A: Yeah, no!\nB: Oooh yeeah!");
    fflush(stdout);
    __isoc99_scanf("%1s",&option);
    if (option == 'A') {
      puts("This Gen Alpha...lol. Tell me, what do you do in your free time if not learning ML?");
      fflush(stdout);
      getchar();
      fgets(buffer,0x100,stdin);
    }
    else if (option == 'B') {
      puts(
          "Yeah, that dude! We\'ll use his ML papers to get control of the world again. Be seeing yo u :)"
          );
    }
    else {
      puts("Sorry, invalid option. Let\'s try this again, shall we?");
    }
  }
  else {
    if (option == 'B') {
      puts("Why shouldn\'t you?");
                    /* WARNING: Subroutine does not return */
      exit(0);
    }
    if (option == 'C') {
      puts("Sure. Learn a few things about him and come back :)");
    }
    else {
      if (option == 'D') {
        puts("Finally! Someone of culture!");
                    /* WARNING: Subroutine does not return */
        exit(0);
      }
      puts("Sorry, invalid option. Let\'s try this again, shall we?");
    }
  }
  return;
}

```

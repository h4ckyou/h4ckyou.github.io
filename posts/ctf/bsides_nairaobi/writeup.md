<h3> Bsides Nairobi 2023 </h3>

### Pwn Challenge Writeup:
- Conundrum
- Simple

This challenges were made by @mug3njutsu and I really enjoyed solving it :)

### Conundrum

Attached file: [link](https://github.com/h4ckyou/h4ckyou.github.io/blob/main/posts/ctf/bsides_nairaobi/Conundrum/conundrum.zip)

We are given a zip file which contained a binary, libc and ld file when decompressed

First thing I did was to patch the binary using [pwninit](https://github.com/io12/pwninit) so as to make sure the binary uses the same libc as the remote instance does 

Now I checked the file type and protections enabled on it
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/6838a330-70e3-4c2f-8127-6d179b3dbe66)

So we're working with a x64 binary which is dynamically linked and not stripped

And from the result gotten from running `checksec` we can see that all protections are enabled!

I ran the binary to get an overview of what it does
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/d40b9ea8-d6a6-4846-a987-b47b3870dcde)

Hmmmm it seems to receive our input and prints it out back

To find the vulnerability I decompiled the binary in Ghidra and here's the main function
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/ad0a4ac6-8ca0-45ae-b5e6-7ac9ec462ff9)

```c
undefined8 main(void)

{
  long in_FS_OFFSET;
  char choice [5];
  long canary;
  
  canary = *(long *)(in_FS_OFFSET + 0x28);
  setup();
  write(1,&DAT_00100b70,0xbb);
  read(0,choice,5);
  if (choice[0] == '1') {
    puts("Go back to where you came!");
                    /* WARNING: Subroutine does not return */
    exit(0);
  }
  if (choice[0] == '2') {
    question();
    write(1,"You wanna tell me a little bit more about pointers?(y/n): ",0x3a);
    read(0,choice,5);
    if (choice[0] == 'y') {
      question();
    }
    else if (choice[0] == 'n') {
      puts("Cheers mate!!");
    }
    else {
      puts("It\'s either yay or nay :)");
    }
    if (canary != *(long *)(in_FS_OFFSET + 0x28)) {
                    /* WARNING: Subroutine does not return */
      __stack_chk_fail();
    }
    return 0;
  }
  puts("It\'s either 1 or 2 :)");
                    /* WARNING: Subroutine does not return */
  exit(0);
}
```

So.... if we choose the first option it would just exit which is not so helpful

And the next choice is option 2 which would call the `question()` function

Here's the pseudo code for the function
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/ebb0b3b3-04ce-4231-bc83-356c1b8d42a3)

```c
void question(void)

{
  long in_FS_OFFSET;
  char buffer [136];
  long canary;
  
  canary = *(long *)(in_FS_OFFSET + 0x28);
  memset(buffer,0,0x80);
  write(1,"Educate me, what\'s so interesting about pointers: ",0x32);
  read(0,buffer,256);
  printf(buffer);
  if (canary != *(long *)(in_FS_OFFSET + 0x28)) {
                    /* WARNING: Subroutine does not return */
    __stack_chk_fail();
  }
  return;
}
```

What this does is basically:
- Defines a buffer which can hold up to 136 bytes
- Reads in at most 256 bytes of our input which is going to be stored in the buffer
- Uses printf to print out our provided input

Looking at the code they are two obvious vulnerability:
- Buffer overflow
- Format string bug

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

There's a buffer overflow because it reads in at most 256 bytes of input which is stored in a buffer that can only hold up 136 bytes giving us an extra 120 bytes to write. And the format string bug exists because it prints out our input without using a format specifier

So what now?

Well after the function is called we are given the choice to call it again

```c
write(1,"You wanna tell me a little bit more about pointers?(y/n): ",0x3a);
read(0,choice,5);
if (choice[0] == 'y') {
  question();
}
else if (choice[0] == 'n') {
  puts("Cheers mate!!");
}
```

What next? How do we go about exploitation!

Because `FULL RELRO` is enabled this means the global offset table is just read only which we can confirm by looking at the memory mapping in gdb
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/94968d22-70ed-45ae-9ac6-5c4d862cfb2b)

The values in the got are in that binary address range which has just `read` permission set on it, so `Got Overwrite` isn't liable 

What next?

Well since there's a buffer overflow we can just overwrite the instruction pointer to jump to a one_gadget

The catch there is that Canary is watching 👀 which would prevent us from doing a stack based overflow

But that isn't an issue because we can use the format string bug to leak the canary

The idea of canary is simple in the sense that it would generate a random value which would be stored on the stack and later compared before the program returns
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/c7f37dbd-2a1f-4732-8c73-dc87316f52c8)
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/3761d60a-366a-4499-81e9-46ef3bce1e6e)

So the canary is placed after our input buffer meaning if we do an overflow it would overwrite the value stored in the canary and when the comparism which checks if the canary still has it's right value is done at the time the program wants to return it would return `False` because we have overwritten it therefore it calls the `__stack_chk_fail` function

The way to go around this is to overwrite the canary to it's right value this is going to be possible because we can leak the canary via the format string bug

One thing about canary which can be used to identify it is that it ends with a null byte `00` 
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/e47468c2-5497-4f7f-808c-41c578718ecb)

Now let's do the good stuff :)

The exploit chain is simple:
- Leak canary and libc address
- Buffer overflow to jump to one_gadget in libc

To do the leak I wrote a fuzz script which basically leaks values off the stack and shows me it's offset

Here's the fuzz script: [link](https://github.com/h4ckyou/h4ckyou.github.io/blob/main/posts/ctf/bsides_nairaobi/Conundrum/fuzz.py)

Running it gives this
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/350b7e76-1eb9-4f2a-be00-aa84493bd3e7)

From the result being leaked off the stack we can see that at offset 23 hold the canary value which we can confirm it being right 
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/b1ff62ca-facf-4ff5-8f08-1726dc46d93c)
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/b00bbdda-3552-42a6-8014-88bcd9329530)

And at offset 29 holds some libc address value
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/29699e4a-f353-4239-92b3-ecd1f154d250)
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/f54eee93-e2ac-4166-8ee8-7e18a07dcacc)

If we have a libc leak we can calculate the libc base address by subtracting it with (known leak - known libc base)
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/8f215432-ade3-48e8-b225-0fce6dbb6012)

At this point we should have the libc base address now we need to make use of the buffer overflow to overwrite the RIP to a one_gadget
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/7ca8e801-c85f-429a-8696-7018eac173a3)

That's all!

So the final thing is to overwrite the canary with it's original value and you can easily get the offset from looking at Ghidra stack layout
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/d1b6959e-2314-4a42-8a44-b97839f182ba)


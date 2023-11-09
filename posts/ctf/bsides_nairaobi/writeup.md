<h3> Bsides Nairobi 2023 </h3>

### Pwn Challenge Writeup:
- Conundrum
- Simple

This challenges were made by @mug3njutsu and I really enjoyed solving it :)

### Conundrum

Attached file: [link](https://github.com/h4ckyou/h4ckyou.github.io/blob/main/posts/ctf/bsides_nairaobi/Conundrum/conundrum.zip)

We are given a zip file which contained a binary, libc and ld file when unzipped

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

At this point we should have the libc base address now we need to make use of the buffer overflow to overwrite the RIP to a one gadget
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/7ca8e801-c85f-429a-8696-7018eac173a3)

That's all!

So the final thing is to overwrite the canary with it's original value and you can easily get the offset from looking at Ghidra stack layout
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/d1b6959e-2314-4a42-8a44-b97839f182ba)

The offset to reach the canary is `0x98 - 0x10 = 0x88`, then we need to overwrite saved rbp with random values since it's not going to be later used and then finally the return address to the one gadget address

Here's the final exploit script: [link](https://github.com/h4ckyou/h4ckyou.github.io/blob/main/posts/ctf/bsides_nairaobi/Conundrum/solve.py)

Running it would spawn a shell 
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/d249ff5a-8a50-4f43-af54-b5a0c22670fc)


### Simple

Attached file: [link](https://github.com/h4ckyou/h4ckyou.github.io/blob/main/posts/ctf/bsides_nairaobi/Simple/simple.zip)

We are given a zip file which contained a binary, libc and ld file when unzipped

I basically followed the same process I did in this first binary challenge (patching, file type & protection)

But later on you will see there's no need to patch the binary to use the remote libc it's just a good practice I guess 🤔

Checking the file type and the protection enabled on the binary shows this
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/177e9587-9e39-43bb-807e-e9a5fd952353)

So we're working with a x64 binary which is dynamically linked and not stripped

The only protection not enabled is "Canary"

I ran the binary to get an overview of what it does
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/38c52af8-8717-4c13-a2d6-3eefc64b47e2)

So it's clear that it would receive our input twice while the first one prints our input back and the second one just receives our input and exit

On decompiling the binary with Ghidra here's the main function
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/56c3a3b2-1d03-4627-bd3b-e52ab25b9ca1)

```c
undefined8 main(void)

{
  undefined8 buffer;
  undefined8 local_50;
  undefined8 local_48;
  undefined8 local_40;
  undefined8 local_38;
  undefined8 local_30;
  undefined8 local_28;
  undefined8 local_20;
  code *notcalled;
  undefined8 *ptr;
  
  setup();
  ptr = (undefined8 *)mmap((void *)0x999999000,0x1000,3,0x21,-1,0);
  notcalled = ::notcalled;
  fwrite("Tell me, what\'s your strategy here: ",1,0x24,stdout);
  read(0,&buffer,64);
  printf("Riiiiight, %s",&buffer);
  *ptr = buffer;
  ptr[1] = local_50;
  ptr[2] = local_48;
  ptr[3] = local_40;
  ptr[4] = local_38;
  ptr[5] = local_30;
  ptr[6] = local_28;
  ptr[7] = local_20;
  fwrite("This might actually come to fruition. Try fire it up: ",1,0x36,stdout);
  fgets((char *)&buffer,200,stdin);
  return 0;
}
```

Here's what it does:
- Sets up a virtual memory space at address `0x999999000` of size `0x1000` with `PROC_READ & PROC_WRITE` permission
- Then it receives our input which reads at most 64 bytes of our input and stored in the buffer
- It uses printf to display the buffer content
- It does some variable assigning and I don't really know the reason :(
- Uses fgets to read in input to the buffer which reads in at most 200 bytes

Looking at this we can tell there's a buffer overflow during the time it receives our input the second time

But we can't do anything for now because PIE is enabled

There's a way to leak it and that's through using printf since it receives 64 bytes of our input, and the thing about printf is that it would print until receiving a null byte

Looking at the stack after it receives the first input I saw this
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/d3ef6f98-38ed-4658-a9dc-ae8619e31a76)

So if we are to fill up the buffer it would overwrite the null byte then printf would leak that `notcalled` function address

And the amount of bytes to fill up the buffer is 64 before we can leak the `notcalled` function address
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/3235db39-035a-4400-be72-5a515fd0ff67)




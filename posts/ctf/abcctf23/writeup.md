<h3> ABCCTF Final 2023 Writeup </h3>

Hi everyone, in this writeup I'll give just the solution of the challenges which had one solve and was blooded by me

### Reveal (Binary Exploitation)
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/789b992c-9104-4523-a619-9ea9ce03de54)

We are given a netcat instance and a zip file 

After downloading the zip file and unzipping it I got this
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/2670ce77-db25-450e-8845-2026d8e4a54e)

So it has a binary and it's libc file

Since this is given I patched the binary to use that libc because that's what going to be running on the remote instance 

I patched it using [pwninit](https://github.com/io12/pwninit)

Time to start the real deal here :P

Checking the file type and protections enabled on the binary shows this
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/aceced47-955e-4550-afbc-bf821519ee24)

We're working with a x64 binary which is dynamically linked and not stripped

All protections are enabled on this binary 💀

I decided to run it to get an idea of what it does
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/d5d288bc-4795-49a4-9123-5d50ce235321)

Cool it seems to receive our input twice

Inorder to find the vulnerability we need to decompile the binary

At first when I used Ghidra and viewed the main function I got this
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/9400b066-f28f-4c51-b6fa-bbfe9e0ee4b5)

```c

undefined8 main(void)

{
  undefined buffer [56];
  long canary;
  
  setup();
  canary = 0x13371337132763b7;
  write(1,
        "Tell me something thrilling and i\'ll share my dirty little secrets, nothing porn related t hough xD: "
        ,100);
  read(0,buffer,0x40);
  printf("You: %s",buffer);
  write(1,"Please, do tell me more, i\'m dying to find out: ",0x30);
  read(0,buffer,100);
  if (canary != 0x13371337132763b7) {
                    /* WARNING: Subroutine does not return */
    __stack_chk_fail();
  }
  return 0;
}
```

- Ok looking at that we can see that it assigns 56 bytes to a buffer and then it stores up a value in the `canary` variable and receives `0x40` bytes of our input which is stored in the buffer
- Our input is then put to stdout using `printf` 
- Then it receives 100 bytes of our input which is stored in the buffer
- It then compares the value stored in `canary` with `0x13371337132763b7`

From this they are two vulnerability:
- We can leak the canary value because the first input receives `0x40 (64)` bytes which is stored in the buffer and the buffer can hold up only 56 bytes so we have additional 8 bytes to overwrite then later on the buffer is displayed using `printf`
- 













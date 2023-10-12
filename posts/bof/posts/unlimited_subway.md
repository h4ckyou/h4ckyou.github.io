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



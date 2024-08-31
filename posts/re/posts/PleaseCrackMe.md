<h3> PleaseCrackMe Crackmes </h3>

![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/77d54fb0-3ae7-4471-a9c9-37ddc50a22ce)

File Checks: 
![Pasted image 20230527231715](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/5b232423-86a2-4922-a417-273aa508c7b0)

We're working with a x64 binary which has all protections enabled on it and it is nt stripped and dynamically linked 

Decompiling with ghidra shows the main function
![Pasted image 20230527231858](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/bd2a61b5-f783-49a5-95c6-c94bf8e49cce)

Here's the edited version:

```c
undefined8 main(void)

{
  int check;
  undefined8 exit_status;
  size_t len_username;
  ulong counter_;
  long in_FS_OFFSET;
  int number;
  int i;
  char username [32];
  char passwordArray [32];
  char password [24];
  long canary;
  
  canary = *(long *)(in_FS_OFFSET + 0x28);
  printf("Type in your Username: ");
  __isoc99_scanf(&%s,username);
  printf("\nType in a number beetween 1 and 9: ");
  __isoc99_scanf(&%d,&number);
  if (number < 1) {
    puts("\nError: Number is too small");
    exit_status = 0xffffffff;
  }
  else if (number < 10) {
    i = 0;
    while( true ) {
      counter_ = (ulong)i;
      len_username = strlen(username);
      if (len_username <= counter_) break;
      passwordArray[i] = (char)number + username[i];
      i = i + 1;
    }
    printf("\nType in the password: ");
    __isoc99_scanf(&%s,password);
    check = strcmp(passwordArray,password);
    if (check == 0) {
      puts("\nYou are succesfully logged in");
    }
    else {
      puts("\nWrong password");
    }
    exit_status = 0;
  }
  else {
    puts("\nError: Number is too big");
    exit_status = 0xffffffff;
  }
  if (canary != *(long *)(in_FS_OFFSET + 0x28)) {
                    /* WARNING: Subroutine does not return */
    __stack_chk_fail();
  }
  return exit_status;
}
```


From the code we can tell what it does:

- Receives our username which is stored in the username variable
- Receives a number which is between 1 and 9
- Does a while loop that breaks when the length of the username is less than the iterate 
- But while the check isn't meet it saves the addition of the number and each index of our username character in the passwordArray variable

To reverse this is quite easy as we would just make a reverse operation for it

I made a script in python to accomplish that for us

```python
#!/usr/bin/python3

username = 'HackYou'
number = 5
password = ''

for i in username:
	password += chr(ord(i) + number)

print(f'Password:- {password}')
```

Running it gives this
![Pasted image 20230528005511](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/7c74b9c8-e127-4da0-866c-a3561adf0c15)

```
➜  PleaseCrackMe python3 solve.py 
Password:- Mfhp^tz
➜  PleaseCrackMe 
```

So the password when I used *HackYou* as the username and *8* as the number is *Mfhp^tz*

Trying it on the binary works
![Pasted image 20230528005635](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/068a44af-fc92-45e7-9764-2a757bd1819b)

And that's all 👻

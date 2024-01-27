<h2> Binary Exploitation </h2>

    - Chall Name: Ecostorage
     - CTF: THCON22

This was a very cool challenge that took me some amount of hours to solve and I learnt something new while solving it

It shows that not all pwn related challenge involves popping of shells 🐚 as there are other various things one can do while exploiting a vulnerability in a program

Let's start shall we?

First thing I do always is to know what type of file I'm working with and the protections enabled on it
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/481ca51d-f842-4047-9446-7e1ae444c5f1)

Cool we are working with a 64bits binary which is dynamically linked and not stripped

The following protections are enabled:
- Full Relro
- Stack Canary
- No-Execute
- PIE

What a hassle all protections are enabled!!

To get an overview of what the binary does I ran it and got this
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/519ef7e1-a6b7-4b50-a323-23e98dcc241e)

So it seems we can:
- Read File
- Go Premium
- Exit

To figure what privilege or vulnerability this binary provides I decompiled it in Ghidra and here's the main function
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/e736c469-9efc-40b6-bc0b-f17b99bce8d0)
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/1b29bd36-4b94-4d00-9f01-de0ab5e05779)

Note that I already renamed some variable name and changed some data type for a better understanding

```c
void main(void)

{
  int fp;
  size_t null;
  char *env;
  long in_FS_OFFSET;
  int choice;
  int is_premium;
  int coupon_used;
  undefined8 *where;
  undefined8 write;
  char access_token [72];
  undefined8 canary;
  
  canary = *(undefined8 *)(in_FS_OFFSET + 0x28);
  is_premium = 0;
  coupon_used = 0;
  setvbuf(stdout,(char *)0x0,2,0);
  do {
    while( true ) {
      while( true ) {
        menu(is_premium);
        __isoc99_scanf("%d%*c",&choice);
        if (choice != 2) break;
        if (is_premium == 0) {
          printf("Access token: ");
          fgets(access_token,64,stdin);
          null = strcspn(access_token,"\n");
          access_token[null] = 0x0;
          env = getenv("ACCESS_TOKEN");
          fp = strcmp(access_token,env);
          if (fp == 0) {
            is_premium = 1;
            puts("Premium access successfully activated!");
          }
          else {
            fp = strcmp(access_token,"THCON2022");
            if (fp == 0) {
              if (coupon_used == 0) {
                coupon_used = 1;
                puts("Success! Your coupon is valid.");
                puts("Tell us your 2 lucky numbers, you might win a premium access!");
                __isoc99_scanf("%lu %lu%*c",&where,&write);
                *where = write;
                puts("Thank you for playing, we\'ll contact you soon!");
              }
              else {
                puts("You can\'t use your coupon twice!");
              }
            }
          }
        }
        else {
          is_premium = 0;
        }
      }
      if (choice < 3) break;
case_end:
      puts("Unknown option.");
    }
    if (choice == 0) {
                    /* WARNING: Subroutine does not return */
      exit(0);
    }
    if (choice != 1) goto case_end;
    printf("Filename: ");
    fgets(filename,64,stdin);
    null = strcspn(filename,"\n");
    filename[null] = 0;
    if ((is_premium == 0) && (env = strstr(filename,"flag"), env != (char *)0x0)) {
      puts("Forbidden file, go premium to read it!");
    }
    else {
      read_file(is_premium);
    }
  } while( true );
}
```

Now I'll explain the idea of what this does

It basically starts a while loop then shows the `menu` function passing the value of the variable `is_premium` as the parameter
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/5b41fa42-8392-442a-8fe7-9d472f3098c1)

```c
void menu(int is_premium)

{
  puts("-= EcoStorage =-");
  if (is_premium == 0) {
    puts("1. Read file part");
    puts("2. Go premium");
  }
  else {
    puts("1. Read file");
    puts("2. Disconnect");
  }
  puts("0. Quit");
  printf(">> ");
  return;
}
```

So basically if the value in `is_premium` is `0` we can only read file part of attempt to go premium else we can read any file or disconnect and generally quit

Now back to the main function it would receive our choice and if we choose option `0` it exits so nothing good comes from it

```c
if (choice == 0) {
                /* WARNING: Subroutine does not return */
  exit(0);
}
```

So the main thing we will work with is option 1 & 2

Let's understand what option 1 does

The first option basically let's us read a file

```c
if (choice != 1) goto case_end;
printf("Filename: ");
fgets(filename,64,stdin);
null = strcspn(filename,"\n");
filename[null] = 0;
if ((is_premium == 0) && (fp = strstr(filename,"flag"), fp != (char *)0x0)) {
  puts("Forbidden file, go premium to read it!");
}
else {
  read_file(is_premium);
}
```

But the check here does this:
- If the value stored in `is_premium` is equal to `0` and the occurrence of `flag` happens to be in the filename provided we would get an error saying **Forbidden file, go premium to read**

So this means that we can read the flag file if we are a premium user, one thing to note here is that the `filename` is a global variable that has a size of 64

Now let's see the function that reads the file provided
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/1f55d067-193f-4c8a-ad84-e0a1dcf17816)

```c
void read_file(int is_premium)

{
  FILE *fptr;
  size_t __n;
  char *fp;
  long in_FS_OFFSET;
  int i;
  char content [136];
  long canary;
  
  canary = *(long *)(in_FS_OFFSET + 0x28);
  fptr = fopen(filename,"r");
  if (fptr == (FILE *)0x0) {
    puts("Failed to open file.");
  }
  else {
    if (is_premium == 0) {
      puts("File content (12 lines maximum): ");
      i = 0;
      while ((i < 12 && (fp = fgets(content,128,fptr), fp != (char *)0x0))) {
        printf("%s",content);
        i = i + 1;
      }
    }
    else {
      puts("File content: ");
      while (__n = fread(content,1,128,fptr), __n != 0) {
        write(1,content,__n);
      }
    }
    putchar(10);
    fclose(fptr);
  }
  if (canary == *(long *)(in_FS_OFFSET + 0x28)) {
    return;
  }
                    /* WARNING: Subroutine does not return */
  __stack_chk_fail();
}
```

Basically this funtion would check if `is_premium` is `0` and if it is we only get 12 lines from whatever we attempt to read else we get the whole content of the file

So things are really limited is we aren't a premium user

Let's see the functionality that makes us become a premium user

```c
if (is_premium == 0) {
  printf("Access token: ");
  fgets(access_token,64,stdin);
  null = strcspn(access_token,"\n");
  access_token[null] = 0x0;
  env = getenv("ACCESS_TOKEN");
  fp = strcmp(access_token,env);
  if (fp == 0) {
    is_premium = 1;
    puts("Premium access successfully activated!");
  }
  else {
    fp = strcmp(access_token,"THCON2022");
    if (fp == 0) {
      if (coupon_used == 0) {
        coupon_used = 1;
        puts("Success! Your coupon is valid.");
        puts("Tell us your 2 lucky numbers, you might win a premium access!");
        __isoc99_scanf("%lu %lu%*c",&where,&write);
        *where = write;
        puts("Thank you for playing, we\'ll contact you soon!");
      }
      else {
        puts("You can\'t use your coupon twice!");
      }
    }
  }
}
else {
  is_premium = 0;
}
```

So it will receive our input which is the access token then compare it to the value stored in the environment variable `ACCESS_TOKEN` if the comparism returns true we set the `is_premium` value to `1`

Else it will check if our input equals `THCON2022` and if it is, the variable `coupon_used` is set to `1`

Then once it tells us the **coupon is valid** it will receive 2 numbers 

```c
puts("Tell us your 2 lucky numbers, you might win a premium access!");
__isoc99_scanf("%lu %lu%*c",&where,&write);
*where = write;
```

This portion of code gives us a write-what-where (www) primitive meaning we can write to memory using this

Also once we use that function is used we can't use it again because it will check is `coupon_used == 0` before it proceeds to the next instruction.........That means it can only be called once

Now what do we do?

Well at this point my thought process was that:
- How do I become a premium user because if I can become that I can surely read the flag
- How do I take advantage of the write what where primitive

Before I started thinking how to use the www primitive I decided to first get a leak because it's going to be useless unless we have leaks since all protections are enabled

This is how I got my leak...... I read the content of `/proc/self/maps` which holds the memory mapping for the current binary process and the result is it's equivalent to running `vmmap` on `gdb`
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/67385b4d-1f70-40c5-bb2f-c231e48c763a)

Because of restrictions we can only read 12 lines of the file but that's enough because we can get the binary base and libc base from that

You might be wondering that the last line is mapping to the libc path

```
7fbe70e5a000-7fbe70e5d000 rw-p 00000000 00:00 0 
```

But that isn't an issue because we can offset it to get to the libc base by adding `0x3000` 
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/b4b7bf0f-608b-407c-bb11-69120b8fbae5)
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/ef46c2e4-a5eb-4e01-88fb-582b980428f7)
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/70726c4b-b2ab-4903-bbfb-abb615beb40d)

At this point we have our leaks now what do we do 🤔

It seemed really hard because I can't overwrite the value of `is_premium` because no stack leak 

Then I searched up some pwn tricks and came around this [link](https://github.com/Naetw/CTF-pwn-tips#leak-stack-address)

It talks about leaking stack but then on reading it, it became clear that the `environ` value in libc maps to the environment variable in the filesystem.... you can read it up [here](https://www.gnu.org/software/libc/manual/html_node/Program-Arguments.html)













































































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

So this means that we can read the flag file if we are a premium user

Now let's see the function that reads the file provided


































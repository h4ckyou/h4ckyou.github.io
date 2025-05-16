<h1> Hackerlab CTF 2025 </h1>

![image](https://github.com/user-attachments/assets/aa819318-6a88-4392-b2aa-8ac245b4b21f)

Hi, so i participated in this ctf with team `adhoc` and we placed 2nd 🫠
![image](https://github.com/user-attachments/assets/bc7db4f2-d975-44ac-98f8-084a4763c2f5)

Although we solved all challenges, this writeup contains solution to just some of the challenges I solved

I don't have much time to make writeup on everything I did

### Challenges
- NeuroNet Collapse
- Hide and Seek
- HackTrace
- MayDay
- Doctor Doom
- Wetin be this
- Last Dance


#### NeuroNet Collapse
![image](https://github.com/user-attachments/assets/7a101c2b-5414-4756-b874-a5256ef81555)

This was the first "pwn" challenge as they were only in total two pwn challenges

I actually solved this one the next day after it was released cause i was busy 

But hey it was still a bit fun :)

Less talking let's get into the challenge....

We are given an executable called `labyrinthe`, checking the file type and protection enabled on it we get this
![image](https://github.com/user-attachments/assets/0aab73af-2457-4ee9-91c8-7b2687853b95)

So this is a 64 bits executable which is dynamically linked and the only protection enabled is NX and PIE

Running it we get this
![image](https://github.com/user-attachments/assets/45642e94-ceff-4fd3-8266-4fad155e5740)

Now i don't understand French and i didn't really bother translating that

I moved to my decompiler which is IDA and here's the main function

```c
int __fastcall main(int argc, const char **argv, const char **envp)
{
  char v3; // al
  const char *v4; // rdi
  char v5; // bl
  char v6; // al
  intruder_t *v7; // rdx
  char v8; // al
  __int64 v9; // rdi
  agent_t *v10; // rdx
  char c; // al
  __int64 v12; // rdi
  intruder_t *v13; // rdx
  __int64 v14; // rcx
  intruder_t *v15; // rdi
  char v16; // al
  __int64 idx; // rbx
  agent_t *v18; // rax

  *agents = 0LL;
  qword_4090 = 0LL;
  while ( 1 )
  {
    puts(s);
    puts(a1InvoquerUnInt);
    v3 = getc(_bss_start);
    v4 = _bss_start;
    v5 = v3;
    if ( getc(_bss_start) != 10 )
      break;
    switch ( v5 )
    {
      case '1':
        if ( intruder )
          puts(&byte_2340);
        else
          intruder = newIntruder();
        continue;
      case '2':
        if ( intruder )
        {
          puts(&byte_2368);
          c = gg();
          if ( (c - 49) > 2u )
          {
            puts(&byte_265E);
          }
          else
          {
            v12 = (c - 48) - 1;
            if ( agents[v12] )
              (intruder->attack)(v12, argv);
            else
              puts(&byte_2390);
          }
        }
        else
        {
          puts(&byte_2673);
        }
        continue;
      case '3':
        v7 = intruder;
        if ( intruder )
          goto trigger;
        puts(&byte_23B8);
        break;
      case '4':
        if ( intruder )
        {
          puts(&byte_23E0);
          v13 = intruder;
          v14 = 10LL;
          v15 = intruder;
          while ( v14 )
          {
            v15->rand_val = 0;
            v15 = (v15 + 4);
            --v14;
          }
          free(v13);
          intruder = 0LL;
        }
        else
        {
          puts(&byte_2690);
        }
        continue;
      case '5':
        puts(&byte_26AA);
        v16 = gg();
        if ( (v16 - 49) > 2u )
        {
          puts(&byte_2458);
        }
        else
        {
          argv = (v16 - 48);
          idx = argv - 1;
          v18 = agents[idx];
          if ( v18 && v18->in_use )
            printf(&format);
          else
            agents[idx] = newAgent();
        }
        continue;
      case '6':
        v4 = &byte_24B0;
        puts(&byte_24B0);
        v6 = gg();
        if ( (v6 - 49) > 2u )
          goto LABEL_31;
        v7 = agents[(v6 - 48) - 1];
        if ( v7 && v7->in_use )
        {
          if ( intruder )
trigger:
            (v7->terminate)(v4, argv);
          else
            puts(&byte_24D8);
        }
        else
        {
          puts(&byte_26E0);
        }
        break;
      case '7':
        puts(&byte_24F8);
        v8 = gg();
        if ( (v8 - 49) > 2u )
        {
LABEL_31:
          puts(&byte_26C7);
        }
        else
        {
          v9 = (v8 - 48) - 1;
          v10 = agents[v9];
          if ( v10 )
            (v10->purge)(v9, argv);
          else
            puts(&byte_2530);
        }
        break;
      default:
        return 0;
    }
  }
  puts(&byte_2318);
  exit(0);
}
```

Note: I already had renamed the variables and types

Looking through the whole program it's obvious that there's not really anywhere where we can give it our input aside the part where it receives our choice



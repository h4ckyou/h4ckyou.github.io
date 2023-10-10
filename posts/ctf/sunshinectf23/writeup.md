<h3> Sunshine CTF 2023 </h3>

![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/5c85ce84-845f-47ee-8dbf-a8caa05439eb)

Hi, I participated in this CTF with a friend of mine and it was a fun one :P

In this writeup I'll give to the solution to the challenges I solved

### Challenges Solved:

#### Cryptography
-  BeepBoop Cryptography

#### Reversing
- Dill

#### Scripting
- DDR
- SimonProgrammer1

#### Web
- BeepBoop Blog
- Hotdog Stand

#### Pwn
- Array of Sunshine
- Flock of Seagulls


#### Cryptography (1/1)

#### BeepBoop Cryptography
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/772c0b6b-8a41-4572-9734-dfea44b80a2e)

After downloading the attached file on checking it's content gave this
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/39c5eeea-e5b9-4c87-9d2c-b29515ed6f41)

If you notice it you'll see that there are only just two words having multiple occurrence

So what I did was to replace `beep` to `0` and `boop` to `1` then convert to string

Here's the script I wrote to do that:

```python
#!/usr/bin/python3

fp = open('BeepBoop').read().split()
cnt = ''

for i in range(len(fp)):
    if fp[i] == 'beep':
        fp[i] = '0'
    else:
        fp[i] = '1'
    
for i in range(0, len(fp), 8):
    cnt += chr(int(''.join(fp[i:i+8]), 2))

print(f"Decoded: {cnt[1::]}")
```

But after running it the result wasn't the flag? 
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/380fa0af-4049-40bf-939f-c6aa3c4dde60)

Ok at least it has the flag format `sun{^.*}` so I assumed this to be some sort of cipher and on using cyberchef I got it to be `rot13`

So here's the final script to get the flag: [solve](https://github.com/h4ckyou/h4ckyou.github.io/blob/main/posts/ctf/sunshinectf23/BeepBoop/solve.py)

```python
#!/usr/bin/python3
import codecs

fp = open('BeepBoop').read().split()
cnt = ''

for i in range(len(fp)):
    if fp[i] == 'beep':
        fp[i] = '0'
    else:
        fp[i] = '1'
    
for i in range(0, len(fp), 8):
    cnt += chr(int(''.join(fp[i:i+8]), 2))

flag = codecs.decode(cnt[1::], 'rot13')
print(f"Flag: {flag}")
```

Running it gives the flag
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/bbab6682-465d-4151-b4a0-8f85d9d509be)

```
Flag: sun{exterminate-exterminate-exterminate}
```

#### Reversing (1/2)

#### Dill
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/9970b6df-9463-4027-8b10-c6024858421f)

After downloading the attached file on checking the file type shows this
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/8a2561b6-8697-4bca-bbc1-351719de04a1)

So that's a python compiled binary whose version is 3.8

We can decompile it using [uncompyle6](https://github.com/rocky/python-uncompyle6) 

Doing that I got this decompiled python code
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/9f80ef84-2b57-4e04-a597-126608848cfc)

```python
class Dill:
    prefix = 'sun{'
    suffix = '}'
    o = [5, 1, 3, 4, 7, 2, 6, 0]

    def __init__(self) -> None:
        self.encrypted = 'bGVnbGxpaGVwaWNrdD8Ka2V0ZXRpZGls'

    def validate(self, value: str) -> bool:
        return value.startswith(Dill.prefix) and value.endswith(Dill.suffix) or False
        value = value[len(Dill.prefix):-len(Dill.suffix)]
        if len(value) != 32:
            return False
        c = [value[i:i + 4] for i in range(0, len(value), 4)]
        value = ''.join([c[i] for i in Dill.o])
        if value != self.encrypted:
            return False
        return True
```

Looking at this we can see that it defines a class object called `Dill` and some variables such as `prefix, suffix, o` are created, the encrypted flag is also given

The validate function of this program does this:
- First if the content of the value passed into this functon doesn't start with `sun{` and ends with `}` it will return `False`
- But if that isn't the case it will extract the value of the flag without it's prefix and suffix i.e removes `sun{}` from our provided value
- Then if the length of the extracted value isn't 32 it will return `False`
- But if it is, it will stored 4 chunks each in the array `c` of our extracted value
- Then it will map the chunk index value to the value being iterated on the array `o` and the result is stored in `value`
- The final result is then compared to the encrypted value, if it isn't the same it returns `False` else it returns `True`

Here's my solve script which just basically maps the encrypted value to it's right index position: [solve](https://github.com/h4ckyou/h4ckyou.github.io/blob/main/posts/ctf/sunshinectf23/Dill/solve.py)

```python
#!/usr/bin/python3

encrypted = 'bGVnbGxpaGVwaWNrdD8Ka2V0ZXRpZGls'
mapping = [5, 1, 3, 4, 7, 2, 6, 0]
prefix = "sun{"
suffix = "}"

enc = [encrypted[i:i+4] for i in range(0, len(encrypted), 4)]
r = [0]*8

for idx, value in enumerate(mapping):
    r[value] = enc[idx]

r = ''.join(r)
flag = prefix + r + suffix

print(f"Flag: {flag}")
```

Running it I got the flag
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/36f9097a-a19e-487b-a820-6439c766763d)

To confirm it's the right flag we can pass it into the `Dill.validate()` [function](https://github.com/h4ckyou/h4ckyou.github.io/blob/main/posts/ctf/sunshinectf23/Dill/validate.py)
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/7a88e436-2d2b-43cc-a3fe-719918d04ef9)

Running it return `True` which means that's the right value
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/c5bb1e19-bbe8-4e71-86fc-b0b113ed240d)

```
Flag: sun{ZGlsbGxpa2V0aGVwaWNrbGVnZXRpdD8K}
```


#### Scripting (2/4)

#### DDR
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/58c19279-c30d-41a2-8482-c0ac78a641f1)

We are given a remote instance to connect to

After connecting to the remote instance via netcat it showed this
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/96824576-91c6-4f57-b288-41e820071db6)

```
Welcome to DIGITAL DANCE ROBOTS!

       -- INSTRUCTIONS --       
 Use the WASD keys to input the 
 arrow that shows up on screen. 
 If you beat the high score of  
     255, you win a FLAG!     

   -- Press ENTER To Start --
```

After pressing the `ENTER` key it showed this
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/a39b9539-f850-4baa-83fc-1b230dc8e866)

From reading it you can just get what we're to do

The goal is that we need to send the received arrow corresponding character key which are `W,A,S,D`. We're to repeat this process `255` times

First when I tried it I spent some time before I got it to work because the way it was doing `I/O` was weird to me but I eventually got it work

So my solution is simple and it involves basically grabbing the arrows, then iterate through every arrow in the arrows and map it to a hashtable (dictionary) containing it's corresponding key value

Then I send the concatenated result to the server for evaluation

Here's the result from running it:
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/1e3dffc4-2d85-4737-8c7f-da27264e9495)

I ran it with pwntools debug mode because I was too lazy to fix the code then :(

So I had to fix it well and on running the updated one you should get this
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/09dc8c52-8c05-466b-a33a-77d4d99bb738)

Here's the solve script: [solve](https://github.com/h4ckyou/h4ckyou.github.io/blob/main/posts/ctf/sunshinectf23/DDR/solve.py)

```
Flag: sun{d0_r0b0t5_kn0w_h0w_t0_d4nc3}
```

#### Web (2/2)

#### BeepBoop Blog 

![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/e0d845a8-b52f-41ab-ab94-690bc77913ec)

Going over to the web url shows this
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/37ee4a15-8b1b-45d6-bfc1-848366131116)

Viewing page source shows this
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/946fa41b-248c-4393-a801-f220907ff67e)

After reading the javascript included I saw this
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/c379c51f-0007-4f9f-81b7-2dfd1d017a73)
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/0c0043bc-0486-4d4d-85d1-06c5ae3ca4d0)

So basically going over to `/posts` should return the list of posts in json

But from the challenge description there's a secret draft and we need to find it

I wasn't the one who solved this but `@Theory`

Here's his solve script: [solve](https://github.com/h4ckyou/h4ckyou.github.io/blob/main/posts/ctf/sunshinectf23/BeepBoop/blog.sh)

```sh
#!/bin/bash

url_base="https://beepboop.web.2023.sunshinectf.games/post/"
i=0

while true; do
    url="$url_base$i"
    response=$(curl -skS -L "$url")
    hidden_value=$(echo "$response" | jq -r '.hidden')
    
    if [[ $hidden_value == "true" ]]; then
        echo "Found a response with hidden: true at $url"
        echo "$response"
        break
    else
        echo "No luck at $url"
        i=$((i + 1))
    fi
done
```


After running it we'll get the hidden post which holds the flag
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/3e09e641-421e-4383-b4be-1bdbb8898e3e)

So frustrating bash so slow well it's using curl so I guess that's the reason :)

```
Flag: sun{wh00ps_4ll_IDOR}
```

#### Hotdog Stand
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/7164a393-26a1-4bbf-8328-ae1abfbd82f9)

Going over to the url shows this
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/c810f087-b5f8-4f9c-b350-92f66d89b81c)

We have a login page, on checking `/robots.txt` reveals this
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/cc7e081d-906c-48c1-97f2-40a5186336f8)

The first two directories are invalid but the third one downloaded a file

The file type is a sqlite database
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/7528e14a-4f92-4014-973e-3e0ba9fe8947)

The number of tables there are 4
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/65fb07c9-3ff5-4a54-a3db-b3369e8be5aa)

The credential table looks interesting and on dumping it I got credential
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/c69a5708-15f2-4cf6-a7f3-3538df12bcde)

```
Username: hotdogstand
Password: slicedpicklesandonions
```

We can use this cred to login on the webapp
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/c0c96446-550e-4c43-bb3b-3b7181174d00)

This was also solved by `@Theory`

Cool that's all for the web pretty easy 

```
Flag: sun{5l1c3d_p1cKl35_4nd_0N10N2}
```

#### Pwn (2/5)

#### Array of Sunshine
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/161b4184-bff4-487f-8d11-987f530c5cd9)

After downloading the binary checking the file type shows this
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/23bad8e4-f3f1-4fe3-83f1-e266d35b0c05)

So we're dealing with a x64 binary which is dynamically linked and not stripped

The protections enabled are `Canary & NX` 

I ran the binary to get an overview of what it does
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/c41310de-87f9-4178-a7f4-2462df2527d4)

Ok it asks for a fruit we want to eat then asks what we want to replace it with

This looks already like a write what where (arbitrary write) sort of challenge

To identify the vulnerability I decompiled it in Ghidra

Here's the decompilation of the main function
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/7163cc13-8c4f-492f-83d9-c4c2e7cd3f9f)

```c
void main(void)

{
  printf_sym = sym_lookup("printf");
  scanf_sym = sym_lookup("scanf");
  logo();
  do {
    basket();
  } while( true );
}
```

- So it calls `sym_lookup` to look up the got value of `printf & scanf` and the resulting value is stored in the global variable `*_sym`
- It then calls the `logo()` function which just prints out that fruit
- In a while loop it calls the `basket()` function

Here's the decompiled code
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/5d522bcb-e86a-4bdb-8b12-14a5c50bbe89)

```c
void basket(void)

{
  long in_FS_OFFSET;
  int fruit;
  undefined *local_30;
  undefined *local_28;
  long local_20;
  undefined8 local_18;
  long canary;
  
  canary = *(long *)(in_FS_OFFSET + 0x28);
  printf("\nWhich fruit would you like to eat [0-3] >>> ");
  __isoc99_scanf("%i",&fruit);
  printf("Replace it with a new fruit.\n",(&fruits)[fruit]);
  printf("Type of new fruit >>>");
  __isoc99_scanf("%24s",&fruits + fruit);
  local_30 = &printf;
  local_28 = &scanf;
  local_20 = _printf;
  local_18 = _scanf;
  if ((printf_sym == _printf) && (printf_sym == _printf)) {
    if (canary != *(long *)(in_FS_OFFSET + 0x28)) {
                    /* WARNING: Subroutine does not return */
      __stack_chk_fail();
    }
    return;
  }
                    /* WARNING: Subroutine does not return */
  exit(-1);
}
```

- First it asks for a fruit we would like to eat and it's gonna receive our input as an integer which is stored in the fruit variable let's take that as `idx`
- Then it asks us what we would want to replace it with and receives 24 bytes of our input as a string which is stored in the `fruit[idx]`
- It compares the value of `print_sym` to the value stored in `_printf` which is the got of `printf` the logic is done again (pretty weird I'll say why this happens later)
- Does the canary check and returns
- But if the comparison returns false it would exit

The global variable `fruits` contains 4 values
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/f36ed0f6-1794-4503-842d-22b024fc95e1)

This is how it looks like in IDA, pretty neat right?
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/38a3d17d-1c93-43aa-bad6-d03efd770d26)

There's also a win function which would give us the flag
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/a7e4b322-f65e-4279-a6c7-a93fa83e8b7c)

So from this I was able to identify this:
- We have Out of Bound (OOB) write because the receive fruit function of this binary doesn't check if the `idx` is within the length of the fruit arrays

But now what can we overwrite or what should we do?

Remember that after running the binary initially it exited instead of calling itself again due to the while loop why is that so?

To know the reason, we know that it can only happen if the got check returns false so let's set a breakpoint there
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/b75c93ad-e54b-420a-a774-e8b13f4ba37a)
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/947eb8b4-0089-436a-bbce-41dcb640a96c)
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/19a82c59-ed62-4db2-86e2-95f74573f6be)
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/14bb25e5-b46b-4df4-9362-ebe322a95c6f)

From the result we can see that the resolved value from the `lookup_symbols` returned got of `printf` i.e `printf@got` which is in the `rdx` register while what it's being compared with is the value stored in the address `0x404020` which is `0x6` 

So that's the reason our it exited because the comparison is false

During the ctf I didn't notice there was a more easier way to solve this but anyways here's what I did

First I needed a way to control the value of `printf_sym` so I can overwrite it with `0x6` so that the comparison returns True and we hit the while loop

To calculate that I calculated the offset from the global variable `fruits` to `printf_sym`

I used `gdb`
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/356b48c2-77dc-4326-bf03-f8f878e4b81b)
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/0c0b45ee-0d20-4ff1-b17e-33dfb3be27dd)
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/e3e454ea-4355-47c8-8eef-34fa2b6ba9e7)

Cool we can see our replaced value which is 8 A's in the 0th index of the fruits array.

Then at the offset 10 is the value of `printf_sym`

We can also just calculate that if we know the addresses of the two values 
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/3718d1fb-2237-4308-b44d-280cabda3f7f)

Now that we have a relative offset to the `printf_sym` address we can overwrite it using the write what where primitive

Here's the helper function for that
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/40972376-7c83-4e94-bea8-e48e653c483c)

At this point we know that the binary will keep looping

So what next?

The idea is that we want to call the win function right?

But that is only possible if any of the function to be called is replaced to the win function

So if we overwrite an address that's supposed to be calling another address and that address is used in the `basket` function then we can overwrite it

At this point I realised I didn't need to overwrite `printf_sym` because `exit@plt` will be called

And because `exit@got ---> exit@plt` that means we can overwrite `exit@got` to the `win` function

But we've already gotten our self in a while loop so I just decided to overwrite `printf@got` to the `win` function

Here's my solve script: [solve]()

Running it works
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/0a9c7b30-4cb6-4b63-b476-86a7031d0a32)

If we run it in a debugger attached to it's current process we will see that `printf@got` is going to call `win`
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/c0c07004-0299-4258-979b-5c83add2a4da)

We can run it remotely to get the flag
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/f9b2f4f8-8868-4f16-94b8-a998c77f0153)

```
Flag: sun{a_ray_of_sunshine_bouncing_around}
```




























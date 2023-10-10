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

I ran it with pwntools debug mode because I'm too lazy to fix the code :(

```
Flag: sun{d0_r0b0t5_kn0w_h0w_t0_d4nc3}
```

#### SimonProgrammer1
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/e55dc15f-1928-4c36-ac3a-58cb1971913a)
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/4e235b4a-ffc5-4c58-bda1-e487ae65ae23)
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/0440990b-0f4e-4022-81da-9abfd27555c6)

So much words in the description (literally every challenges lol), anyways going over to the web url shows this









































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

So here's the final script to get the flag

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



















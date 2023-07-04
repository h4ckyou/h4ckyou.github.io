<h3> BattleCTF Prequal 2023 </h3>

#### Description: This was a fun ctf I participated in as an individual player. Thanks to the organizers for the awesome challenges
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/b550193f-987a-48ca-a355-bf5a0948eeef)

<h3> Challenge Solved </h3>

## Misc
- Discord
- Way
- Go
- Minon Agbodo
- BUG|PWN
- php zlib

## Web
- Civilization
- Own Reality
- It shock you
- Cobalt Injection
- Africa
- Hebiossa Injection
- Cobalt Injection2
- Perfect Timing

## Forensics
- Thumb
- Find Me
- Africa Beauty
- Minon
- Base64
- Gift
- TorrentVerse

## PWN
- AM1
- youpi
- AXOVI
- 0xf

## Reverse Engineering
- SEYI
- Welcome
- babyrev
- checker
- Mazui

## Cryptography
- Back To Origin
- Blind
- Gooss

### Misc 6/7 :~

#### Discord
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/5ac8e231-b339-4e3a-a8d1-dc7f1ff504ef)

After joining the discord channel and viewing the `announcement` I saw the flag
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/940d1887-ff3e-4e20-ac84-fe8a238df8ab)

```
Flag: battleCTF{WeLoveAfrica}
```

#### Way
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/d94fc0b5-1d30-40c2-a13c-008eb815ad59)

After downloading the attached file checking the file type shows it is a zip file archive
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/7772ffbf-77f1-44ab-a3c9-683c6f29f00a)

I tried to unzip it but I got this
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/1150a6fc-d214-46b5-8784-867a30b2c535)

With this I know that it will require a password if I try to unzip using `7z` 

So let us brute force the password

I converted it to a format john can understand using `zip2john`
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/e50380b7-2602-41d0-b61a-729d0372adb7)

The password is `samoanpride` 

Let us unzip it now
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/579712f5-75bf-4a95-b906-92bd86623a17)

It unzipped to form an image file

Checking the image shows the `BUG|PWN` logo
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/2f45845b-ce17-4586-8cb7-c068d185a2e4)

Using strings showed me the password and from there I can filter it to get the last line in which the password is
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/bd029b3b-2adb-4356-83ee-21ff6f2cedc9)

```
Flag: battleCTF{The_Best_Way_To_Learn}
```

### GO
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/c7f019e1-3187-4ce6-b003-4357c5e2bb32)

It gave this string:

```
onggyrPGS{RaqGvzr_vf_terng}
```

I used [dcoder.fr](https://www.dcode.fr/cipher-identifier) to identify the type of cipher it is
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/b35a9c43-b1ee-410d-8fed-d6440f69a292)

It says it is `ROTed` 

I then decoded it using [this](https://www.dcode.fr/rot-13-cipher) 
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/6f8d3b6c-4a99-4885-ab55-76a2f8d0dd66)

```
Flag: battleCTF{EndTime_is_great}
```

### Minon Agbodo 
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/9e0a1365-e094-45cd-9daf-02c8ac596d99)

We are given ssh credential to login with

After I logged in using:

```
ssh battlectf@chall.battlectf.online -p 30000 -oHostKeyAlgorithms=+ssh-dss
```

I saw this
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/714bbd60-0564-473d-9287-b2271f2a1873)

Seems we are in a restriced environment!!

I ran `bash` and it seemed to broke out of it
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/93503b8a-c0f2-41a1-94e8-09927afc44b9)

Still I can't run commands

After playing with some characters I figured using command injection payloads work quite well

And I got the flag that way
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/3f7223d0-89e8-494e-8cc2-0fe7fe035ffc)

```
Flag: battleCTF{Agb0d0_J4!L_Awhouangan}
```

### BUG|PWN
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/6da61151-dfca-43c6-b4af-b3c1e25c0a94)

After going to the twitter page of the [BUG|PWN](https://twitter.com/0xbugpwn/status/1672272446257340417) organizers I found some hex values
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/7cdc216a-76b3-40bc-bd7b-bf492785032b)

Well those hex values are the messages while the key is the founder's name `RAVEN` 

I wrote a script to decode it 🙂

```python
#!/usr/bin/env python3
from pwn import xor
import warnings
warnings.filterwarnings('ignore')

cipher = b'\x0e\x39\x60\x77\x12\x2a\x77\x67\x19\x36\x65\x75\x0a\x3d\x79\x66\x1d\x2e\x73\x2d\x0e\x39\x60\x70\x12\x2a\x75\x65\x19\x36\x67\x75\x0a\x3d\x7a\x64\x1d\x2e\x72\x2c\x0e\x39\x62\x77\x12\x2a\x74\x63\x19\x36\x66\x76\x0a\x3d\x79\x31\x1d\x2e\x70\x7e\x0e\x39\x63\x72\x12\x2a\x75\x33\x19\x36\x67\x27\x0a\x3d\x7a\x31\x1d\x2e\x73\x28\x0e\x39\x61\x73\x12\x2a\x77\x63\x19\x36\x65\x72\x0a\x3d\x7b\x34\x1d\x2e\x70\x7b\x0e\x39\x65\x75\x12\x2a\x76\x6e\x19\x36\x61\x71\x0a\x3d\x79\x6a\x1d\x2e\x72\x2a'
key = b'RAVEN'

xored = xor(cipher, key).decode()
print(f'H3X: {xored}')

## LINKS ##
# https://twitter.com/bug_pwn/status/1672272446257340417
# https://twitter.com/w31rdr4v3n
```

Running it decodes to this
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/2a326366-bc8c-4eac-9d72-ed17f5d0947b)

For some reason python `bytes.fromhex` doesn't work on it so I used cyberchef
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/00362a5a-ed3c-4398-8ea4-6fb7e97b7874)

```
Flag: battleCTF{BUG|PWN_Loves_U0x0x}
```

###  php zlib 
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/b6ed939a-441d-40d4-8e38-e4d027c49531)

We are given the source and also the web service url

To be honest I didn't take a look at the source 😃

After going to the web service I saw the header to be this
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/bbca78f0-8f50-4232-95c7-6e17d2524c78)

The user agent header value looks interesting:

```
PHP/8.1.0-dev
```

Searching for exploits leads [here](https://www.exploit-db.com/exploits/49933)

Running it works and we are root on the docker container
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/17618b4f-b19a-4d7d-9e91-ed328c17e351)

But the flag isn't there. 

I then used `find` command to get the path to where the flag is 
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/b2a06d38-e047-429f-b036-118bd6fbfbef)

And now we can get it's content
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/22a95025-8df5-4c33-a701-395eea578a80)

```
Flag: battleCTF{phP_useragentt_l1kes_wahala_1357f40569024191137a63aa10098f60}
```

### Web 8/10 :~

#### Civilization
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/5c8c1db4-b900-4284-b233-7290325bb062)

Going over to the web service shows this
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/afd0b9b2-5275-46c1-9a42-03749fc372fb)
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/61070af0-fe48-4b1a-8bbe-b737c7fc072e)

Since the text says we should get the source code by going to `/?source` let us get it
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/3594b883-6a0a-4782-a942-e2f025923cd0)

From the page source we get this:

```php
<?php
require("./flag.php");
if(isset($_GET['source'])){
    highlight_file(__FILE__);  
}
if(isset($_GET['ami'])){
    $input = $_GET['ami'];
    $cigar = 'africacradlecivilization';
    if (preg_replace("/$cigar/",'',$input) === $cigar) {
        africa();
    }
}
include("home.html");
?>
```

We can tell what it does:
- Checks if the GET parameter `ami` is set
- If it returns true then the value of the parameter is set as the `input` variable
- The text `africacradlecivilization` is set as the cigar variable
- It does a preg replace on the value of input and cigar
- If the value formed after preg replace is done is equal to the cigar value we get the into the africa function which should likely contain the flag

From this we know that we need to make the input value to be `africacradlecivilization` in order to get the flag

But the issue is after preg_replace is done it will check that input is it contains `africacradlecivilization` and replace it with null values

How do we bypass it?

We can do this:

```
africaafricacradlecivilizationcradlecivilization
```

Now after preg replace removes the `africacradlecivilization` from that string it then forms `africacradlecivilization` 

Let us get the flag now
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/58d511e7-a965-4d01-af0a-7e0d124d8c36)

```
Flag: battleCTF{pr3gr4plAcebyp455_0x0x0x0x}
```


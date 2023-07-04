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

## Binary Exploitation
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

#### Own Reality
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/51a08221-339b-47b7-8c06-ea1a13b25026)

Going over to the web page shows this
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/0ad76c5b-c73b-4893-90af-d577132b7942)

Immediately my `DogGit` firefox extension showed that there's an exposed `/.git` 
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/421f8c9a-9c1f-47e0-8603-4cffe31eaa85)

Going over to `/.git` shows that it is indeed there
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/69909769-e643-41b8-aafc-eaecf938f115)

I'll use `git-dumper` to dump the git repo
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/9b25ff75-45ee-4847-97df-ba5c713d6b4b)

Now that is done let us check the commit using `git log`
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/2710bb92-76c7-44df-9d62-7a3577d33d3a)

I can view the commit `a1346a3abab8f97748e5480b61eb6824d4692f44` using `git show a1346a3abab8f97748e5480b61eb6824d4692f44`
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/cbdfca62-5b6b-4daf-bd81-8bff15df7675)

We can see this:

```
.__..._..__...._.___._...___._...__.__...__.._._._....__._._._..._...__..____.__._._._._.__.___..__._.__.__.___..__.____.___.___.__.___.._._____.__..._..__._.._.___._...___..__._._____..__..__..___.....__._...__.._._.__.._._.__...._..__._....___.._.__..._...__._....__..._..__.___.__.._._.__.._._..__.._..__..__..__..__...__._._.__...._..__..._..__..__.__..__..__..._..__.._...__...__.__...__.__...._..__.__..__..__...__..__..__.._...__.___._____._
```

It looks like morse code but after decoding it from morse doesn't give the flag

After trying hours on this I then tried to convert the dots to 0 and underscores to 1

I wrote a script to do that

```python
#!/usr/bin/python

encoded = ".__..._..__...._.___._...___._...__.__...__.._._._....__._._._..._...__..____.__._._._._.__.___..__._.__.__.___..__.____.___.___.__.___.._._____.__..._..__._.._.___._...___..__._._____..__..__..___.....__._...__.._._.__.._._.__...._..__._....___.._.__..._...__._....__..._..__.___.__.._._.__.._._..__.._..__..__..__..__...__._._.__...._..__..._..__..__.__..__..__..._..__.._...__...__.__...__.__...._..__.__..__..__...__..__..__.._...__.___._____._"
decode1 = encoded.replace('.', '0')
decode2 = decode1.replace('_', '1')
print(decode2)
```

Running it gives this
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/e9d31f9c-35da-4e93-b926-dc96a8610598)

Using cyberchef to decode it gives the flag
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/29e490f5-58ee-402b-8683-a825721bf188)

```
Flag: battleCTF{Unknown_bits_384eea49b417ee2ff5a13fbdcca6f327}
```

#### It shock you 
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/4eade6ff-12de-4a35-8c2b-b25f8e39ba5f)

Going over to the web service shows this
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/83028fb3-6437-49d9-a59d-7432ebcaa598)

The apache version looks interesting
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/4aad0eea-1625-400b-b54d-5ba9fea5ed2c)

```
Apache/2.4.49
```

Searching for exploits leads [here](https://github.com/CalfCrusher/Path-traversal-RCE-Apache-2.4.49-2.4.50-Exploit/blob/main/main.py) 

From the source it does a directory transversal by using `.%2e`

Running the exploit shows it works
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/e2c8a909-5c37-4d65-9437-01866f89bc78)
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/a8cf47c8-090c-4e57-bf6d-7c3c4d945cf4)

Since we want to look for the flag I decided to do it manually
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/25157e23-1276-4fe8-a2b6-8cdfef83262a)

The flag is at `/flag.txt` but when I try access it I get 404 error
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/f0a4567f-a41d-4132-90b2-588c65ca9c1e)

So here's what I did

Since we know we can read a direct file `/etc/passwd` I can just go back one directory and get the flag `/etc/passwd/../flag.txt`
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/d34ca430-b485-4b4b-b83a-50ccfc6c103b)

```
Flag: battleCTF{Apache_2.4.49_wahala_26e223dfefdcc5ce214a4b6ad83f5a49}
```

### Cobalt Injection [First Blood 🩸]
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/f68ef9ad-b9be-4d66-914a-55d67d0d2cec)

Going over to the web page shows this
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/9f2aa757-ee37-4504-87c4-4696e1d20d29)

Checking wappalyzer shows it is PHP but is it ?

![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/b78344fa-1490-4571-8c87-1b2d4b42ffd7)

I confirmed using `curl` and it shows it is python werkzeug
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/7b4aa20e-40b7-43fc-ac02-b6e4e4f1bb08)

Now that the web server language is confirmed let us get to solving it

Checking the page source shows how it excepts the capital to be guessed
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/395db72a-a279-439d-92c7-c3a82d0b3e5d)

```
<!-- IP?capital=Benin -->
```

Doing that I noticed this
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/22757e57-ef77-45b8-91c3-6730c1e3df7e)

We can now try SSTI payload since our input value seems to be rendered back

And our payload gets evaluated
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/353e39d9-0f7b-4eec-995f-78531325debc)

Checking the config doesn't really show any thing interesting
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/eb2a9b46-8f71-433f-b8ea-0336b343ca05)

Let us get remote code execution then

I used a payload gotten from [PayloadAllTheThings](https://github.com/swisskyrepo/PayloadsAllTheThings/tree/master/Server%20Side%20Template%20Injection#exploit-the-ssti-by-calling-ospopenread)
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/03fc99de-7789-42b8-9384-ac031310f826)

```
Flag: battleCTF{wahala_1nj3ction_in_country}
```

#### Africa [First Blood 🩸]
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/b070fbc5-d7dc-4018-b0d4-edcccebe54bf)

Going over to the web service shows this
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/92d8cd58-1ff4-4f0b-9944-aef72923d971)

Since this is a http-header based sorta web chall let us play with the header from burp

I changed the `User-Agent` to `africa` and got this
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/eb7baa85-fdab-4ed6-bcb4-b8a3053fa046)

Hmm it's saying that it isn't coming from `local client` 

I can use the `X-Forwarded-For` header
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/7a7dcd7a-4f61-4f46-a76f-327a5fa545cd)

Now I get that error

We can use the `Referer` header for that
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/6a5fb78a-2938-4017-a46b-8f990f7ad446)

Since this is based on the tracking header which is `DNT` 

I'll set it to 1 and I got the flag
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/dc53882f-b987-44f0-8767-2eeb15f7927c)

Instead of doing that manually I made a script for it 

```python
#!/usr/bin/python3
import requests
from bs4 import BeautifulSoup

url = 'http://chall.battlectf.online:8081/'
headers = {
    'User-Agent': 'africa',
    'DNT': '1',
    'X-Forwarded-For': '127.0.0.1',
    'Referer': 'battlectf.online'
}

req = requests.get(url, headers=headers)
reqz = BeautifulSoup(req.text, 'html.parser')
div_tag = reqz.find('div', class_='container')
flag = div_tag.get_text(strip=True)
print(flag)
```

#### Hebiosso injection 

Going over to the web service shows this
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/04e44e8a-6bd4-4b06-a439-d09226606e46)

One thing we can try here is sql injection 🙂

I saved the search request to a file
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/add106d2-7f3b-4f68-88b8-239d5cc0f176)

Now we can use sqlmap to get check it

Doing that shows it is vulnerable to `UNION query` sql injection

Let us get the database present
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/e6ebac90-4f69-4b84-9d4e-15e135f3f32e)
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/410f8dd3-45dc-4d9f-9f6a-0bc72f3c5827)

So the database is `hebiosso` now let us get the tables present
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/b122ac02-3074-424f-8cf8-da43ab4ad5ec)
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/20bd726d-a924-4afe-9fca-acdb1817c72b)

Cool we can now dump the flag table
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/464b7f2e-0c09-4d56-beda-a4a50dbf2e3a)
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/88f75b4e-bfad-4e0e-9a13-3491d12fd65a)

```
Flag: battleCTF{Like_based_SQLi_Fu_0af52e4e8696a3dffe7eea367eeb277d}
```

#### Cobalt Injection 2 [First Blood 🩸]
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/0de00648-9821-4bd5-82e5-cecf0f9bf3bd)

So this is the revenge for `Cobalt Injection 1` 
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/64aba670-3a60-40b1-95c2-aab73e276547)

Trying the basic ssti payload still works
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/0016ed26-1dca-4394-b6bd-47910964e9cd)

But when I try the payload used it doesn't work
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/8a464f6f-770c-4e4a-82d2-224d9fdf6181)

Seems they added like a filter of some sort

After playing with it I figured it filters dot and underscores 

Looking at [this](https://github.com/swisskyrepo/PayloadsAllTheThings/tree/master/Server%20Side%20Template%20Injection#jinja2---filter-bypass)

I got the payload to be used and we can see it worked
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/15f339ef-49ca-40bc-8882-348fdede3d96)

I can now get the flag 
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/08e7d928-8e80-433c-9a08-237a635b21f0)

```
Note: Since dot is filtered I did 'cat flag\x2etxt'
```

And here's the flag

```
Flag: battleCTF{C0untry_1nj3ct!on_f1!73r_Bypass_534d3d21720fbdb1cc1a58e75e25993a}
```

#### Perfect Timing 
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/f3e4f944-f9cd-4729-844f-3bc0c7985a5b)

Going over to the web page shows this login page
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/e6017fb6-3be3-44f2-a6e6-d27ebbd0dd75)

I saved the post request to a file to check for sql injection

And it turned out to be a time based sql injection

Just follow the process I did for `Hebiossa Injection` you will get this
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/74940e68-242d-4f20-b7dd-7a50282da6a7)
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/41204953-0d44-4826-b3c8-ee56c3b35869)

```
Flag: battleCTF{Common_SQLi_Time_558de3659cc32ee7bc9f1745ecd63ae2}
```

### Forensics 7/10 :~

#### Thumb
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/ce53232b-24a1-4274-97c4-ab979bfef7b0)

After downloading the attached file I checked the file type and it is an image file
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/648f120c-056f-4b54-be19-fc62fa0ae80f)

Using binwalk shows there are other jpegs inside the image
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/695e2596-ad67-4d13-b900-93809f838054)

I can extract them all
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/f39100c7-dc55-4b21-af76-c7b928fd90ec)

The extracted files are images
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/a47ba596-682a-408d-86a3-7a39599ec6c4)

The 102 file shows a QRCode
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/a4aff63c-27e4-4c15-a885-a63c485ec86c)

I then used `zbarimg` to decode it
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/2a2f434c-2c56-494b-997f-f87500cfc739)

```
Flag: battleCTF{3XP3C71N6_7HUM8N411_70_83 _41W4Y5_83_H1DD3N}
```

#### Find Me 
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/c08ee672-c462-4116-ae93-303015cd7ff6)

After downloading the attached file shows that it is a wireshark packet file
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/35c2c733-351e-4294-9893-9a9b0801ff3b)

I opened it up in wireshark and check the protocol hierarchy
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/d2e4fead-4a71-4dce-8211-565d2d6b9597)

We can see some HTTP protocol present in the pcapc file

I can now apply it as filter and follow tcp stream

Stream 3 shows this POST request with some login details
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/463a971c-27fa-45fc-a8e3-521d8f3c7f63)

```
userid=hardawayn&pswrd=UEFwZHNqUlRhZQ%3D%3D
```

Decoding it gives the password
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/754547d0-fd7b-4ebc-bc89-fb31c51c21a6)

```
Flag: battleCTF{PApdsjRTae}
```

#### Africa Beauty 
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/8fe26621-e01a-4e79-88f6-44165a606c1e)

From the details it seems we need to get some values from the file attached

The file attached is an image file
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/1d56ba76-659c-43d3-8647-2199dd3ac4c8)

And the details we need are:
- Make
- Camera Model
- Front/Back
- Country
- City

Let us use `exiftool` to get the image metadata
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/0c1131f0-aa8e-4936-bced-a79898f8f98c)
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/9b810f08-704e-4b97-90c0-982668717904)
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/e6640050-65c0-4048-a311-780a7f89e600)

Now we have the:
- Make == Google
- Camera Model == Pixel4XL
- Front/Back == Back

How do we get the country and city?

The metadata also gave the GPS Position to be:

```
6 deg 20' 59.76" N, 2 deg 24' 48.96" E
```

We can use a gps to location checker for this 

And after doing that I got [this](https://www.google.com/maps/place/Boulevard+de+la+Marina,+Cotonou,+Benin/@6.350245,2.4183454,17z/data=!3m1!4b1!4m6!3m5!1s0x102354572323f069:0x55e3471d46e14f66!8m2!3d6.350245!4d2.4183454!16s%2Fg%2F1tggksmn?entry=ttu)
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/1a160781-9fdd-46a7-ba4e-d65f09b860a2)

```
Flag: battleCTF{Google_Pixel4XL_back_Benin_Cotonou}
```

#### Base64
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/56e84680-78de-4571-931d-48d5dc2573a9)

After looking around the platform I found the base64 encoded string [here](https://prequal.battlectf.online/users?page=6)
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/a268c1f2-0466-46fb-bb25-b790a542eef4)

Decoding it gives the flag
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/3142fd8e-4f4a-4f89-99b7-d66c9272e932)

```
Flag: battleCTF{b4s3_64_4_3nc0d1n9}
```

#### GIFt
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/9e93c20e-f777-4b28-a572-5cad31c258b7)

Checking the file type of the attached file shows this
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/c7a44c8b-268c-431f-a645-0321fb19f65f)

It doesn't recognise it cause the file header is messed up 

So I used `xxd` to check the hex dump
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/962af485-bc9c-4f94-ba72-9165c8727c07)

We can see this `NETSCAPE2.0`

After doing research I found that it is a GIF file

And in order to fix it we need to append this to the file header `0x47494638`

I made a script to do that

```python
#!/usr/bin/python3

buf = open('gift.gif', 'rb').read()
buf = b"\x47\x49\x46\x38" + buf
with open('fix.gif', 'wb') as fd:
    fd.write(buf)
```

Now we can check the file type for `fix.gif`
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/812da551-df91-4675-b44f-6eb619a86788)

Opening it shows some text file 
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/95b3d6f4-6209-4d40-9a85-ccd7653ce27a)

But since it is gif it removes and come back and I can't note the word 

So I used stegsolve to extract the frames
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/0b0c02a1-723a-4be1-a8d9-909bb9cd09a7)
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/0765a414-0e65-4bb2-ad42-54bb5ad562d1)
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/5803f266-ad36-44be-8442-23da193e71d9)
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/2f79748b-3c54-45c2-817c-f482342f08c7)
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/1a45f0dd-4ea7-42c7-8a41-4ba87165b82c)

Knowing that I just decoded it 

```python
#!/usr/bin/python3
import base64
s='ZmxhZ3tnMWZfb3JfajFmfQ=='
print(base64.b64decode(s))
```

And got the flag

```
Flag: battleCTF{g1f_or_j1f}
```

### Binary Exploitation 6/10 :~

#### BlackRop
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/ba882ce7-3452-4310-83f7-fb1af63976de)

After downloading the file and unzipping it I got this
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/179782af-8b09-4845-807b-cbf251c439b1)

Source code is given
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/ad2f99d2-d0a8-4980-8336-1daef2abccdd)
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/69f59c40-1a4b-4c1e-8a5f-70ad4f59d4ee)

From the source code we can see the main function calls the vuln function

And the vuln function is vulnerable to buffer overflow since it uses `gets()` to receive our input

```c
void vuln()
{
	char buffer[10];

	printf("check your identity and read the flag.\n");
	gets(buffer);
}
```

There's a win function called read_flag()

```c
void read_flag(){
	if(!(check_file && african && invite_code && capcha)) {
		printf("403|You aren't allowed to read the flag!\n");
		exit(1);
	}
	
	char flag[65];
	FILE * f = fopen("flag.txt","r");
	if (f == NULL){
		printf("flag.txt doesn't exist, try again on the server\n");
		exit(0);
	}
    fgets( flag, 65, f );
    printf("%s\n",flag);
    fflush(stdout);
}
```

But before it works it does a check on the global variables `check_file && african && invite_code && capcha`

And each of those variables are confirmed from other functions 

Like the check_file is set when check_flag function returns true

```c
void check_flag(char* file) {
	if(strcmp(file, "flag.txt") == 0) {
		check_file = 1;
	}
}
```

african is true when the african function returns true

```c
void check_african() {
	african = 1;
}
```

invite_code is true when the check_invitecode function returns true

```c
void check_invitecode(int code) {
	if(code == 0xbae) {
		invite_code = 1;
	}
}
```

capcha is true when the check_capcha function returns true

```c
void check_capcha(int login, int auth) {
	if(login == 0x062023 && auth == 0xbf1212) {
		capcha = 1;
	}
}
```

Since we know there's a buffer overflow that means we can overwrite the return address `EIP` and set it anywhere we like

And in x86 which is the binary architecture arguments are passed from the stack as fun, ret, arg1, arg2... Since the ret address in the next step will confuse the parameter passing, so ret is generally pressed

Now let us get the offset needed to overwrite the instruction pointer and I'll use gdb-gef for it
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/a96785a9-12bc-473d-9bb6-6e86b20171cd)
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/20326d72-1d49-4f85-a8af-c14b3cc0155c)

The offset is 22

I'll also need some pop gadgets
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/6716aad0-55b2-4d8b-a524-23a66877f794)

Here's my exploit [script]()
